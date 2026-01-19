#!/usr/bin/env node
/**
 * ATOM Trail CLI
 * Command-line interface for the ATOM logging system
 * 
 * ATOM: ATOM-CLI-20260119-001-cli-implementation
 */

import { program } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import {
  logATOM,
  queryATOM,
  visualizeATOM,
  exportATOM,
  getATOMStats,
  generateMermaidDiagram
} from './trail-persister.js';
import { ATOMQueryFilters, ATOMExportFormat } from './types.js';

const DEFAULT_TRAIL_PATH = '.spiralsafe/atom-trail.jsonl';

/**
 * Format timestamp for display
 */
function formatTimestamp(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleString();
}

/**
 * Log command - Log a decision manually
 */
program
  .command('log')
  .description('Log a decision to the ATOM trail')
  .argument('<decision>', 'What was decided')
  .requiredOption('--rationale <rationale>', 'Why this decision was made')
  .requiredOption('--outcome <outcome>', 'Decision outcome (success|failure|pending)')
  .option('--vortex <vortex>', 'Vortex ID', 'cli')
  .option('--coherence <score>', 'Coherence score (0-1)', parseFloat)
  .option('--priority <weight>', 'Fibonacci priority (1,2,3,5,8,13...)', parseInt)
  .option('--context <json>', 'Additional context as JSON string', '{}')
  .option('--trail <path>', 'Path to trail file', DEFAULT_TRAIL_PATH)
  .action(async (decision, options) => {
    try {
      const context = JSON.parse(options.context);
      
      const entry = await logATOM({
        vortexId: options.vortex,
        decision,
        rationale: options.rationale,
        outcome: options.outcome,
        coherenceScore: options.coherence,
        fibonacciWeight: options.priority,
        context
      }, options.trail);
      
      console.log(`✓ Logged ATOM entry: ${entry.id}`);
      console.log(`  Timestamp: ${formatTimestamp(entry.timestamp)}`);
      console.log(`  Vortex: ${entry.vortexId}`);
      console.log(`  Outcome: ${entry.outcome}`);
      if (entry.coherenceScore) {
        console.log(`  Coherence: ${(entry.coherenceScore * 100).toFixed(1)}%`);
      }
    } catch (error) {
      console.error(`✗ Error logging entry: ${error}`);
      process.exit(1);
    }
  });

/**
 * Query command - Query the ATOM trail
 */
program
  .command('query')
  .description('Query the ATOM trail with filters')
  .option('--vortex <vortex>', 'Filter by vortex ID')
  .option('--outcome <outcome>', 'Filter by outcome (success|failure|pending)')
  .option('--since <time>', 'Start time (ISO 8601)')
  .option('--until <time>', 'End time (ISO 8601)')
  .option('--min-coherence <score>', 'Minimum coherence score', parseFloat)
  .option('--max-coherence <score>', 'Maximum coherence score', parseFloat)
  .option('--limit <n>', 'Limit results', parseInt, 10)
  .option('--offset <n>', 'Offset for pagination', parseInt, 0)
  .option('--trail <path>', 'Path to trail file', DEFAULT_TRAIL_PATH)
  .action(async (options) => {
    try {
      const filters: ATOMQueryFilters = {
        vortexId: options.vortex,
        outcome: options.outcome,
        startTime: options.since,
        endTime: options.until,
        minCoherence: options.minCoherence,
        maxCoherence: options.maxCoherence,
        limit: options.limit,
        offset: options.offset
      };
      
      const entries = await queryATOM(filters, options.trail);
      
      if (entries.length === 0) {
        console.log('No entries found matching the filters.');
        return;
      }
      
      console.log(`Found ${entries.length} entries:\n`);
      
      entries.forEach((entry, index) => {
        console.log(`${index + 1}. ${entry.decision}`);
        console.log(`   ID: ${entry.id}`);
        console.log(`   Vortex: ${entry.vortexId}`);
        console.log(`   Timestamp: ${formatTimestamp(entry.timestamp)}`);
        console.log(`   Outcome: ${entry.outcome}`);
        if (entry.coherenceScore !== undefined) {
          console.log(`   Coherence: ${(entry.coherenceScore * 100).toFixed(1)}%`);
        }
        if (entry.fibonacciWeight !== undefined) {
          console.log(`   Priority: ${entry.fibonacciWeight}`);
        }
        console.log(`   Rationale: ${entry.rationale}`);
        console.log('');
      });
    } catch (error) {
      console.error(`✗ Error querying trail: ${error}`);
      process.exit(1);
    }
  });

/**
 * Export command - Export the ATOM trail
 */
program
  .command('export')
  .description('Export ATOM trail in various formats')
  .option('--format <format>', 'Export format (json|csv|markdown)', 'markdown')
  .option('--output <file>', 'Output file (default: stdout)')
  .option('--vortex <vortex>', 'Filter by vortex ID')
  .option('--outcome <outcome>', 'Filter by outcome')
  .option('--since <time>', 'Start time (ISO 8601)')
  .option('--until <time>', 'End time (ISO 8601)')
  .option('--trail <path>', 'Path to trail file', DEFAULT_TRAIL_PATH)
  .action(async (options) => {
    try {
      const filters: ATOMQueryFilters = {
        vortexId: options.vortex,
        outcome: options.outcome,
        startTime: options.since,
        endTime: options.until
      };
      
      const format = options.format as ATOMExportFormat;
      const output = await exportATOM(format, filters, options.trail);
      
      if (options.output) {
        await fs.promises.writeFile(options.output, output, 'utf-8');
        console.log(`✓ Exported to ${options.output}`);
      } else {
        console.log(output);
      }
    } catch (error) {
      console.error(`✗ Error exporting trail: ${error}`);
      process.exit(1);
    }
  });

/**
 * Viz command - Visualize the ATOM trail
 */
program
  .command('viz')
  .description('Visualize ATOM trail as a decision graph')
  .argument('<vortex>', 'Vortex ID to visualize')
  .option('--output <file>', 'Output file for Mermaid diagram')
  .option('--trail <path>', 'Path to trail file', DEFAULT_TRAIL_PATH)
  .action(async (vortex, options) => {
    try {
      const graph = await visualizeATOM(vortex, options.trail);
      const mermaid = generateMermaidDiagram(graph);
      
      if (options.output) {
        await fs.promises.writeFile(options.output, mermaid, 'utf-8');
        console.log(`✓ Mermaid diagram saved to ${options.output}`);
      } else {
        console.log(mermaid);
      }
      
      console.log(`\nGraph Statistics:`);
      console.log(`  Total nodes: ${graph.nodes.size}`);
      console.log(`  Root nodes: ${graph.roots.length}`);
    } catch (error) {
      console.error(`✗ Error visualizing trail: ${error}`);
      process.exit(1);
    }
  });

/**
 * Stats command - Show statistics about the ATOM trail
 */
program
  .command('stats')
  .description('Show statistics about the ATOM trail')
  .option('--trail <path>', 'Path to trail file', DEFAULT_TRAIL_PATH)
  .action(async (options) => {
    try {
      const stats = await getATOMStats(options.trail);
      
      console.log('ATOM Trail Statistics\n');
      console.log(`Total Entries: ${stats.totalEntries}`);
      console.log(`  ✓ Success: ${stats.successCount}`);
      console.log(`  ✗ Failure: ${stats.failureCount}`);
      console.log(`  ⋯ Pending: ${stats.pendingCount}`);
      console.log('');
      
      if (stats.avgCoherenceScore > 0) {
        console.log(`Average Coherence: ${(stats.avgCoherenceScore * 100).toFixed(1)}%`);
        console.log('');
      }
      
      console.log('Vortex Breakdown:');
      Object.entries(stats.vortexBreakdown)
        .sort(([, a], [, b]) => b - a)
        .forEach(([vortex, count]) => {
          console.log(`  ${vortex}: ${count} entries`);
        });
      
      if (stats.timeRange.earliest && stats.timeRange.latest) {
        console.log('');
        console.log('Time Range:');
        console.log(`  Earliest: ${formatTimestamp(stats.timeRange.earliest)}`);
        console.log(`  Latest: ${formatTimestamp(stats.timeRange.latest)}`);
      }
    } catch (error) {
      console.error(`✗ Error getting stats: ${error}`);
      process.exit(1);
    }
  });

// Parse command line arguments
program
  .name('atom-trail')
  .description('ATOM (Auditable Trail Of Modifications) CLI')
  .version('1.0.0');

program.parse(process.argv);

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
