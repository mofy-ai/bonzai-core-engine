#!/usr/bin/env python3
"""
🚀 BONZAI BACKEND - PRODUCTION TEST RUNNER
==========================================
Convenient script to run production tests with different options
"""

import os
import sys
import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

def print_banner():
    """Print test runner banner"""
    print("=" * 80)
    print("🚀 BONZAI BACKEND PRODUCTION TEST RUNNER")
    print("=" * 80)
    print(f"📅 Started: {datetime.now()}")
    print("🎯 Purpose: Validate production readiness")
    print("=" * 80)

def setup_arguments():
    """Setup command line arguments"""
    parser = argparse.ArgumentParser(
        description="Run Bonzai Backend production tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_production_tests.py                    # Run all tests
  python run_production_tests.py --quick           # Run critical tests only
  python run_production_tests.py --category api    # Run API tests only
  python run_production_tests.py --backend-url http://localhost:5001
  python run_production_tests.py --output results.json
        """
    )
    
    parser.add_argument(
        '--quick', 
        action='store_true',
        help='Run only critical tests (faster execution)'
    )
    
    parser.add_argument(
        '--category',
        choices=['environment', 'dependencies', 'services', 'variants', 
                'performance', 'quotas', 'integration', 'api', 'memory', 
                'websocket', 'security', 'deployment'],
        help='Run specific test category only'
    )
    
    parser.add_argument(
        '--backend-url',
        default='http://localhost:5001',
        help='Backend URL to test (default: http://localhost:5001)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for test results (default: auto-generated)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--no-api-tests',
        action='store_true',
        help='Skip API endpoint tests (useful if backend is not running)'
    )
    
    return parser.parse_args()

def check_backend_running(backend_url):
    """Check if backend is running"""
    try:
        import requests
        response = requests.get(f"{backend_url}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

async def run_tests(args):
    """Run the production tests"""
    
    # Set environment variable for backend URL
    os.environ['BACKEND_URL'] = args.backend_url
    os.environ['PORT'] = args.backend_url.split(':')[-1]
    
    # Import and run the test suite
    try:
        # Import the test suite
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the main test runner
        if os.path.exists('PRODUCTION_MASTER_TEST_SUITE.py'):
            print("📦 Loading production test suite...")
            import PRODUCTION_MASTER_TEST_SUITE as test_suite
            
            # Check if we should skip API tests
            if args.no_api_tests:
                print("⚠️ Skipping API tests (--no-api-tests specified)")
                # Modify the test suite to skip API tests
                async def skip_api_tests():
                    pass
                test_suite.APITester.test_all = skip_api_tests
            
            # Check backend status if running API tests
            elif not check_backend_running(args.backend_url):
                print(f"⚠️ Backend not responding at {args.backend_url}")
                print("💡 Use --no-api-tests to skip API endpoint testing")
                print("💡 Or start the backend first: python app.py")
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    print("❌ Test execution cancelled")
                    return False
            
            print("🚀 Starting production test execution...")
            
            # Run the main test suite
            await test_suite.main()
            
            print("\n✅ Production test execution completed!")
            return True
            
        else:
            print("❌ Error: PRODUCTION_MASTER_TEST_SUITE.py not found")
            print("💡 Make sure you're in the correct directory")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")
        return False

def generate_summary_report(results_file):
    """Generate a summary report"""
    try:
        if not os.path.exists(results_file):
            print(f"⚠️ Results file not found: {results_file}")
            return
        
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        meta = results.get("meta", {})
        
        print("\n" + "="*60)
        print("📊 TEST EXECUTION SUMMARY")
        print("="*60)
        
        # Overall statistics
        total = meta.get("total_tests", 0)
        passed = meta.get("passed", 0)
        failed = meta.get("failed", 0)
        warnings = meta.get("warnings", 0)
        critical = meta.get("critical_failures", 0)
        
        print(f"📈 Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️ Warnings: {warnings}")
        print(f"🚨 Critical: {critical}")
        
        if total > 0:
            success_rate = (passed / total) * 100
            print(f"📊 Success Rate: {success_rate:.1f}%")
            
            # Determine readiness
            if critical == 0:
                if failed == 0:
                    readiness = "🟢 PRODUCTION READY"
                elif failed < 5:
                    readiness = "🟡 MOSTLY READY"
                else:
                    readiness = "🟠 NEEDS WORK"
            else:
                readiness = "🔴 NOT READY"
            
            print(f"🎯 Status: {readiness}")
        
        print(f"⏱️ Duration: {meta.get('test_duration', 0):.2f}s")
        print("="*60)
        
    except Exception as e:
        print(f"⚠️ Error generating summary: {str(e)}")

def create_test_report():
    """Create a comprehensive test report"""
    
    # Find the most recent test results file
    results_files = []
    for file in os.listdir('.'):
        if file.startswith('production_test_results_') and file.endswith('.json'):
            results_files.append(file)
    
    if not results_files:
        print("⚠️ No test results found")
        return
    
    # Get the most recent file
    latest_file = sorted(results_files)[-1]
    
    try:
        with open(latest_file, 'r') as f:
            results = json.load(f)
        
        # Generate markdown report
        report_file = latest_file.replace('.json', '_REPORT.md')
        
        with open(report_file, 'w') as f:
            f.write("# 🚀 BONZAI BACKEND - PRODUCTION TEST REPORT\n\n")
            f.write(f"**Generated**: {datetime.now().isoformat()}\n")
            f.write(f"**Test File**: {latest_file}\n\n")
            
            meta = results.get("meta", {})
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Tests**: {meta.get('total_tests', 0)}\n")
            f.write(f"- **Passed**: {meta.get('passed', 0)}\n")
            f.write(f"- **Failed**: {meta.get('failed', 0)}\n")
            f.write(f"- **Warnings**: {meta.get('warnings', 0)}\n")
            f.write(f"- **Critical Failures**: {meta.get('critical_failures', 0)}\n")
            f.write(f"- **Duration**: {meta.get('test_duration', 0):.2f} seconds\n\n")
            
            # Category breakdown
            f.write("## 📋 Category Results\n\n")
            for category, tests in results.items():
                if category == "meta" or not isinstance(tests, dict):
                    continue
                
                passed = sum(1 for test in tests.values() 
                           if isinstance(test, dict) and test.get('status') == 'PASS')
                total = len(tests)
                
                if total > 0:
                    rate = (passed / total) * 100
                    f.write(f"### {category.replace('_', ' ').title()}\n")
                    f.write(f"- **Status**: {passed}/{total} ({rate:.0f}%)\n")
                    
                    # List failures
                    failures = [name for name, test in tests.items() 
                              if isinstance(test, dict) and test.get('status') != 'PASS']
                    
                    if failures:
                        f.write(f"- **Issues**: {', '.join(failures[:5])}\n")
                    f.write("\n")
            
            # Critical issues
            f.write("## 🚨 Critical Issues\n\n")
            critical_found = False
            for category, tests in results.items():
                if isinstance(tests, dict):
                    for test_name, test_data in tests.items():
                        if (isinstance(test_data, dict) and 
                            test_data.get('critical') and 
                            test_data.get('status') != 'PASS'):
                            f.write(f"- **{category}/{test_name}**: {test_data.get('message', '')}\n")
                            critical_found = True
            
            if not critical_found:
                f.write("✅ No critical issues found!\n")
            
            f.write("\n## 💡 Recommendations\n\n")
            
            if meta.get('critical_failures', 0) == 0:
                f.write("✅ **System is production ready!**\n")
                f.write("- Address any warnings for optimal performance\n")
                f.write("- Monitor system performance in production\n")
            else:
                f.write("🔴 **System requires attention before production**\n")
                f.write("- Resolve all critical failures first\n")
                f.write("- Run tests again after fixes\n")
        
        print(f"📄 Test report generated: {report_file}")
        
    except Exception as e:
        print(f"⚠️ Error creating test report: {str(e)}")

def main():
    """Main function"""
    args = setup_arguments()
    
    print_banner()
    
    if args.verbose:
        print(f"🔧 Configuration:")
        print(f"   Backend URL: {args.backend_url}")
        print(f"   Quick mode: {args.quick}")
        print(f"   Category: {args.category or 'All'}")
        print(f"   Skip API tests: {args.no_api_tests}")
        print()
    
    # Run the tests
    success = asyncio.run(run_tests(args))
    
    if success:
        # Find and display summary from most recent results
        results_files = [f for f in os.listdir('.') 
                        if f.startswith('production_test_results_') and f.endswith('.json')]
        
        if results_files:
            latest_results = sorted(results_files)[-1]
            generate_summary_report(latest_results)
            
            # Generate comprehensive report
            create_test_report()
            
            print(f"\n📁 Detailed results: {latest_results}")
            print("🎯 Test execution completed successfully!")
        else:
            print("⚠️ No test results file found")
    
    else:
        print("❌ Test execution failed")
        sys.exit(1)

if __name__ == "__main__":
    main()