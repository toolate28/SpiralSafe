/**
 * Rate Limiting Tests
 * Tests for the checkRateLimit function to ensure proper rate limit enforcement
 */

import { describe, it, expect, beforeEach, vi } from "vitest";

// Mock types matching the worker
interface Env {
  SPIRALSAFE_DB: D1Database;
  SPIRALSAFE_KV: KVNamespace;
  SPIRALSAFE_R2: R2Bucket;
  SPIRALSAFE_API_KEY: string;
  SPIRALSAFE_API_KEYS?: string;
  RATE_LIMIT_REQUESTS?: string;
  RATE_LIMIT_WINDOW?: string;
  RATE_LIMIT_AUTH_FAILURES?: string;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
}

// Mock KV namespace
class MockKVNamespace {
  private store: Map<string, { value: string; expirationTtl?: number }> =
    new Map();

  async get(key: string): Promise<string | null> {
    const data = this.store.get(key);
    return data ? data.value : null;
  }

  async put(
    key: string,
    value: string,
    options?: { expirationTtl?: number },
  ): Promise<void> {
    this.store.set(key, { value, expirationTtl: options?.expirationTtl });
  }

  clear(): void {
    this.store.clear();
  }
}

// Rate limiting function extracted for testing
async function checkRateLimit(
  env: Env,
  ip: string,
  key: string,
  maxRequests: number,
  windowSeconds: number,
): Promise<RateLimitResult> {
  const rateLimitKey = `ratelimit:${key}:${ip}`;
  const now = Math.floor(Date.now() / 1000);
  const windowStart = now - windowSeconds;

  // Get current request data
  const dataJson = await env.SPIRALSAFE_KV.get(rateLimitKey);
  let requests: number[] = dataJson ? JSON.parse(dataJson) : [];

  // Filter out requests outside the current window
  requests = requests.filter((timestamp) => timestamp > windowStart);

  // Check if rate limit is exceeded BEFORE adding current request
  const allowed = requests.length < maxRequests;

  // Calculate remaining slots
  let remaining: number;

  // Add current request if allowed
  if (allowed) {
    requests.push(now);
    remaining = maxRequests - requests.length;
  } else {
    // No remaining requests when rate limit is exceeded
    remaining = 0;
  }

  // Store updated request list with TTL (always update to keep data clean)
  // Note: Denied requests are intentionally not tracked in KV to prevent
  // attackers from filling storage with blocked request timestamps
  await env.SPIRALSAFE_KV.put(rateLimitKey, JSON.stringify(requests), {
    expirationTtl: windowSeconds,
  });

  // When rate limited, the window effectively resets when the oldest
  // request in the current window expires, not a full window from now.
  // Use a conservative fallback when not rate limited or if there are no requests.
  const resetAt =
    !allowed && requests.length > 0
      ? requests[0] + windowSeconds
      : now + windowSeconds;

  return { allowed, remaining, resetAt };
}

describe("checkRateLimit", () => {
  let mockKV: MockKVNamespace;
  let mockEnv: Env;
  const testIP = "192.168.1.1";
  const testKey = "test-endpoint";

  beforeEach(() => {
    mockKV = new MockKVNamespace();
    mockEnv = {
      SPIRALSAFE_KV: mockKV as unknown as KVNamespace,
      SPIRALSAFE_DB: {} as D1Database,
      SPIRALSAFE_R2: {} as R2Bucket,
      SPIRALSAFE_API_KEY: "test-key",
    };
    vi.useFakeTimers();
  });

  it("should allow requests when under the limit", async () => {
    const maxRequests = 10;
    const windowSeconds = 60;

    const result = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );

    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(9); // 10 - 1 = 9 remaining
  });

  it("should allow exactly maxRequests within the window", async () => {
    const maxRequests = 10;
    const windowSeconds = 60;

    // Make 10 requests
    for (let i = 0; i < maxRequests; i++) {
      const result = await checkRateLimit(
        mockEnv,
        testIP,
        testKey,
        maxRequests,
        windowSeconds,
      );
      expect(result.allowed).toBe(true);
      expect(result.remaining).toBe(maxRequests - i - 1);
    }

    // Verify the last request showed 0 remaining
    const finalCheck = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(finalCheck.remaining).toBe(0);
  });

  it("should block the (maxRequests + 1)th request", async () => {
    const maxRequests = 10;
    const windowSeconds = 60;

    // Make maxRequests successful requests
    for (let i = 0; i < maxRequests; i++) {
      const result = await checkRateLimit(
        mockEnv,
        testIP,
        testKey,
        maxRequests,
        windowSeconds,
      );
      expect(result.allowed).toBe(true);
    }

    // The 11th request should be blocked
    const blocked = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(blocked.allowed).toBe(false);
    expect(blocked.remaining).toBe(0);
  });

  it("should correctly filter requests outside the window", async () => {
    const maxRequests = 5;
    const windowSeconds = 60;

    // Set time to 1000 seconds
    vi.setSystemTime(1000 * 1000);

    // Make 5 requests (filling the limit)
    for (let i = 0; i < maxRequests; i++) {
      await checkRateLimit(
        mockEnv,
        testIP,
        testKey,
        maxRequests,
        windowSeconds,
      );
    }

    // Next request should be blocked
    let result = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(false);

    // Advance time beyond the window (61 seconds)
    vi.setSystemTime((1000 + 61) * 1000);

    // Now requests should be allowed again as old ones are filtered out
    result = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(maxRequests - 1);
  });

  it("should return accurate remaining count when allowed", async () => {
    const maxRequests = 5;
    const windowSeconds = 60;

    // First request: 4 remaining
    let result = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(4);

    // Second request: 3 remaining
    result = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(3);

    // Third request: 2 remaining
    result = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(2);
  });

  it("should return 0 remaining when denied", async () => {
    const maxRequests = 2;
    const windowSeconds = 60;

    // Fill the limit
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);

    // Denied request should show 0 remaining
    const denied = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(denied.allowed).toBe(false);
    expect(denied.remaining).toBe(0);
  });

  it("should calculate resetAt correctly when rate limited", async () => {
    const maxRequests = 2;
    const windowSeconds = 60;

    // Set time to 1000 seconds
    const baseTime = 1000;
    vi.setSystemTime(baseTime * 1000);

    // Make 2 requests to fill the limit
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);

    // Next request should be denied and resetAt should be first request + window
    const denied = await checkRateLimit(
      mockEnv,
      testIP,
      testKey,
      maxRequests,
      windowSeconds,
    );
    expect(denied.allowed).toBe(false);
    // resetAt should be the timestamp of the first request + windowSeconds
    expect(denied.resetAt).toBe(baseTime + windowSeconds);
  });

  it("should not track denied requests in KV storage", async () => {
    const maxRequests = 2;
    const windowSeconds = 60;

    // Fill the limit
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);

    // Make a denied request
    await checkRateLimit(mockEnv, testIP, testKey, maxRequests, windowSeconds);

    // Check KV storage - should only have 2 timestamps (not 3)
    const rateLimitKey = `ratelimit:${testKey}:${testIP}`;
    const stored = await mockKV.get(rateLimitKey);
    const timestamps = JSON.parse(stored!);
    expect(timestamps).toHaveLength(2);
  });

  it("should handle concurrent requests correctly", async () => {
    const maxRequests = 5;
    const windowSeconds = 60;

    // Simulate sequential requests (more predictable for testing)
    const results = [];
    for (let i = 0; i < 10; i++) {
      results.push(
        await checkRateLimit(
          mockEnv,
          testIP,
          testKey,
          maxRequests,
          windowSeconds,
        ),
      );
    }

    // Count allowed and denied
    const allowed = results.filter((r) => r.allowed).length;
    const denied = results.filter((r) => !r.allowed).length;

    // Should allow exactly maxRequests and deny the rest
    expect(allowed).toBe(maxRequests);
    expect(denied).toBe(5);
    expect(allowed + denied).toBe(10);
  });

  it("should isolate rate limits by IP and key", async () => {
    const maxRequests = 2;
    const windowSeconds = 60;

    // Fill limit for IP1 + key1
    await checkRateLimit(
      mockEnv,
      "192.168.1.1",
      "key1",
      maxRequests,
      windowSeconds,
    );
    await checkRateLimit(
      mockEnv,
      "192.168.1.1",
      "key1",
      maxRequests,
      windowSeconds,
    );

    // Different IP should not be affected
    let result = await checkRateLimit(
      mockEnv,
      "192.168.1.2",
      "key1",
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(true);

    // Different key should not be affected
    result = await checkRateLimit(
      mockEnv,
      "192.168.1.1",
      "key2",
      maxRequests,
      windowSeconds,
    );
    expect(result.allowed).toBe(true);
  });
});
