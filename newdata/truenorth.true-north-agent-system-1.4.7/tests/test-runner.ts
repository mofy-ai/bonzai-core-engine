#!/usr/bin/env node

import { spawn } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface TestSuite {
  name: string;
  command: string;
  timeout: number;
  required: boolean;
  parallel?: boolean;
}

interface TestResult {
  suite: string;
  success: boolean;
  duration: number;
  output: string;
  error?: string;
}

class TestRunner {
  private results: TestResult[] = [];
  private startTime: number = Date.now();

  private readonly testSuites: TestSuite[] = [
    {
      name: 'Lint',
      command: 'npm run lint',
      timeout: 30000,
      required: true
    },
    {
      name: 'TypeScript Compilation',
      command: 'npm run compile',
      timeout: 60000,
      required: true
    },
    {
      name: 'Unit Tests',
      command: 'npm run test:unit',
      timeout: 120000,
      required: true,
      parallel: false
    },
    {
      name: 'Integration Tests',
      command: 'npm run test:integration',
      timeout: 180000,
      required: true,
      parallel: false
    },
    {
      name: 'WebSocket Tests',
      command: 'npm run test -- tests/unit/websocket',
      timeout: 60000,
      required: true,
      parallel: true
    },
    {
      name: 'Performance Tests',
      command: 'npm run test:performance',
      timeout: 300000,
      required: false,
      parallel: true
    },
    {
      name: 'Security Tests',
      command: 'npm run test:security',
      timeout: 120000,
      required: true,
      parallel: true
    },
    {
      name: 'End-to-End Tests',
      command: 'npm run test:e2e',
      timeout: 300000,
      required: false,
      parallel: false
    }
  ];

  async runSuite(suite: TestSuite): Promise<TestResult> {
    console.log(`🧪 Running ${suite.name}...`);
    const startTime = Date.now();

    return new Promise((resolve) => {
      const child = spawn('sh', ['-c', suite.command], {
        stdio: ['inherit', 'pipe', 'pipe'],
        env: { ...process.env, CI: 'true' }
      });

      let output = '';
      let errorOutput = '';

      child.stdout?.on('data', (data) => {
        output += data.toString();
        process.stdout.write(data);
      });

      child.stderr?.on('data', (data) => {
        errorOutput += data.toString();
        process.stderr.write(data);
      });

      const timeout = setTimeout(() => {
        child.kill('SIGTERM');
        console.log(`⏰ ${suite.name} timed out after ${suite.timeout}ms`);
      }, suite.timeout);

      child.on('close', (code) => {
        clearTimeout(timeout);
        const duration = Date.now() - startTime;
        const success = code === 0;

        const result: TestResult = {
          suite: suite.name,
          success,
          duration,
          output,
          error: success ? undefined : errorOutput
        };

        if (success) {
          console.log(`✅ ${suite.name} passed (${duration}ms)`);
        } else {
          console.log(`❌ ${suite.name} failed (${duration}ms)`);
          if (errorOutput) {
            console.log(`Error: ${errorOutput.slice(0, 500)}...`);
          }
        }

        resolve(result);
      });

      child.on('error', (error) => {
        clearTimeout(timeout);
        const duration = Date.now() - startTime;
        
        console.log(`💥 ${suite.name} errored: ${error.message}`);
        
        resolve({
          suite: suite.name,
          success: false,
          duration,
          output,
          error: error.message
        });
      });
    });
  }

  async runParallelSuites(suites: TestSuite[]): Promise<TestResult[]> {
    console.log(`🔄 Running ${suites.length} test suites in parallel...`);
    
    const promises = suites.map(suite => this.runSuite(suite));
    return Promise.all(promises);
  }

  async runSequentialSuites(suites: TestSuite[]): Promise<TestResult[]> {
    const results: TestResult[] = [];
    
    for (const suite of suites) {
      const result = await this.runSuite(suite);
      results.push(result);
      
      // Stop on critical failures
      if (!result.success && suite.required) {
        console.log(`🛑 Critical test suite failed: ${suite.name}`);
        break;
      }
    }
    
    return results;
  }

  async runAllTests(): Promise<void> {
    console.log('🚀 Starting TrueNorth Test Suite...\n');

    // Separate suites by execution strategy
    const parallelSuites = this.testSuites.filter(s => s.parallel);
    const sequentialSuites = this.testSuites.filter(s => !s.parallel);

    // Run sequential suites first (critical path)
    const sequentialResults = await this.runSequentialSuites(sequentialSuites);
    this.results.push(...sequentialResults);

    // Check if we should continue with parallel suites
    const criticalFailures = sequentialResults.filter(r => !r.success && 
      sequentialSuites.find(s => s.name === r.suite)?.required
    );

    if (criticalFailures.length === 0) {
      // Run parallel suites
      const parallelResults = await this.runParallelSuites(parallelSuites);
      this.results.push(...parallelResults);
    } else {
      console.log('⚠️ Skipping parallel tests due to critical failures');
    }

    this.generateReport();
  }

  private generateReport(): void {
    const totalDuration = Date.now() - this.startTime;
    const totalSuites = this.results.length;
    const passedSuites = this.results.filter(r => r.success).length;
    const failedSuites = this.results.filter(r => !r.success).length;

    console.log('\n' + '='.repeat(80));
    console.log('📊 TEST SUITE SUMMARY');
    console.log('='.repeat(80));
    
    console.log(`Total Duration: ${(totalDuration / 1000).toFixed(2)}s`);
    console.log(`Total Suites: ${totalSuites}`);
    console.log(`Passed: ${passedSuites} ✅`);
    console.log(`Failed: ${failedSuites} ❌`);
    console.log(`Success Rate: ${((passedSuites / totalSuites) * 100).toFixed(1)}%`);

    console.log('\n📋 Detailed Results:');
    this.results.forEach(result => {
      const status = result.success ? '✅' : '❌';
      const duration = (result.duration / 1000).toFixed(2);
      console.log(`  ${status} ${result.suite.padEnd(30)} ${duration}s`);
    });

    // Generate JSON report
    const report = {
      timestamp: new Date().toISOString(),
      totalDuration,
      summary: {
        total: totalSuites,
        passed: passedSuites,
        failed: failedSuites,
        successRate: (passedSuites / totalSuites) * 100
      },
      results: this.results
    };

    const reportPath = path.join(process.cwd(), 'test-results.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\n📄 Report saved to: ${reportPath}`);

    // Generate coverage summary if available
    this.generateCoverageSummary();

    // Exit with appropriate code
    const exitCode = failedSuites === 0 ? 0 : 1;
    if (exitCode === 0) {
      console.log('\n🎉 All tests passed!');
    } else {
      console.log('\n💥 Some tests failed!');
    }
    
    process.exit(exitCode);
  }

  private generateCoverageSummary(): void {
    const coveragePath = path.join(process.cwd(), 'coverage', 'coverage-summary.json');
    
    if (fs.existsSync(coveragePath)) {
      try {
        const coverage = JSON.parse(fs.readFileSync(coveragePath, 'utf8'));
        const total = coverage.total;
        
        console.log('\n📈 Coverage Summary:');
        console.log(`  Lines: ${total.lines.pct}%`);
        console.log(`  Functions: ${total.functions.pct}%`);
        console.log(`  Branches: ${total.branches.pct}%`);
        console.log(`  Statements: ${total.statements.pct}%`);
        
        // Check coverage thresholds
        const minCoverage = 80;
        const coverageOk = total.lines.pct >= minCoverage && 
                          total.functions.pct >= minCoverage &&
                          total.branches.pct >= minCoverage &&
                          total.statements.pct >= minCoverage;
        
        if (coverageOk) {
          console.log('  ✅ Coverage thresholds met');
        } else {
          console.log(`  ❌ Coverage below ${minCoverage}% threshold`);
        }
      } catch (error) {
        console.log('  ⚠️ Could not read coverage summary');
      }
    }
  }

  async runCoverageTests(): Promise<void> {
    console.log('📊 Running tests with coverage...');
    
    const result = await this.runSuite({
      name: 'Coverage Tests',
      command: 'npm run test:coverage',
      timeout: 300000,
      required: true
    });

    this.results = [result];
    this.generateReport();
  }

  async runSpecificSuite(suiteName: string): Promise<void> {
    const suite = this.testSuites.find(s => 
      s.name.toLowerCase().includes(suiteName.toLowerCase())
    );

    if (!suite) {
      console.log(`❌ Test suite not found: ${suiteName}`);
      console.log('Available suites:');
      this.testSuites.forEach(s => console.log(`  - ${s.name}`));
      process.exit(1);
    }

    console.log(`🎯 Running specific test suite: ${suite.name}`);
    const result = await this.runSuite(suite);
    this.results = [result];
    this.generateReport();
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const runner = new TestRunner();

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
TrueNorth Test Runner

Usage:
  npm run test                    Run all tests
  npm run test:coverage           Run tests with coverage
  npm run test:suite <name>       Run specific test suite
  
Options:
  --help, -h                      Show this help message

Available test suites:
  - lint
  - unit
  - integration  
  - websocket
  - performance
  - security
  - e2e
    `);
    process.exit(0);
  }

  if (args.includes('--coverage')) {
    await runner.runCoverageTests();
  } else if (args.includes('--suite') && args[args.indexOf('--suite') + 1]) {
    const suiteName = args[args.indexOf('--suite') + 1];
    await runner.runSpecificSuite(suiteName);
  } else {
    await runner.runAllTests();
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error('💥 Test runner failed:', error);
    process.exit(1);
  });
}

export { TestRunner };