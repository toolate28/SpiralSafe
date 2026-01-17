import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      include: ["api/**/*.ts"],
      exclude: ["api/**/*.test.ts", "api/**/__tests__/**"],
    },
  },
});
