#!/usr/bin/env python3
"""
🔥 ULTIMATE MEM0 TEST - Quick validation of all components
"""

import os
import sys
import time
from datetime import datetime

def test_imports():
    """Test if all required imports are available"""
    print("🔥 TESTING ULTIMATE MEM0 IMPORTS...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from flask_cors import CORS
        print("✅ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"❌ Flask-CORS import failed: {e}")
        return False
    
    try:
        import redis
        print("✅ Redis imported successfully")
    except ImportError as e:
        print(f"❌ Redis import failed: {e}")
        return False
    
    try:
        from mem0 import MemoryClient
        print("✅ Mem0 imported successfully")
    except ImportError as e:
        print(f"❌ Mem0 import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True

def test_redis_connection():
    """Test Redis connection"""
    print("\n🔥 TESTING REDIS CONNECTION...")
    
    try:
        r = redis.Redis(
            host='redis-16121.c304.europe-west1-2.gce.redns.redis-cloud.com',
            port=16121,
            decode_responses=True,
            username="default",
            password="m3JA7FrUS7rplQZMR6Nmqr7mCONV7pEQ",
        )
        
        # Test connection
        result = r.ping()
        if result:
            print("✅ Redis connection successful!")
            
            # Test basic operations
            r.set('test_key', 'ultimate_mem0_test')
            value = r.get('test_key')
            if value == 'ultimate_mem0_test':
                print("✅ Redis read/write operations working!")
                r.delete('test_key')
                return True
            else:
                print(f"❌ Redis read/write failed: expected 'ultimate_mem0_test', got '{value}'")
                return False
        else:
            print("❌ Redis ping failed")
            return False
            
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
        return False

def test_mem0_client():
    """Test Mem0 client initialization"""
    print("\n🔥 TESTING MEM0 CLIENT...")
    
    try:
        from mem0 import MemoryClient
        client = MemoryClient()
        print("✅ Mem0 client initialized successfully!")
        
        # Test basic memory operation
        try:
            result = client.add(
                messages=[{"role": "user", "content": "Ultimate Mem0 test message"}],
                user_id="test_user"
            )
            print("✅ Mem0 add operation successful!")
            
            # Test search
            search_results = client.search(
                query="Ultimate Mem0 test",
                user_id="test_user"
            )
            print(f"✅ Mem0 search operation successful! Found {len(search_results)} results")
            
            return True
            
        except Exception as e:
            print(f"❌ Mem0 operations failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Mem0 client initialization failed: {e}")
        return False

def test_flask_app():
    """Test basic Flask app creation"""
    print("\n🔥 TESTING FLASK APP CREATION...")
    
    try:
        from flask import Flask, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/')
        def test_endpoint():
            return jsonify({
                'status': 'Ultimate Mem0 Test Successful!',
                'timestamp': datetime.now().isoformat(),
                'features': ['All imports working', 'Redis connected', 'Mem0 initialized']
            })
        
        print("✅ Flask app created successfully!")
        print("✅ CORS configured successfully!")
        print("✅ Test endpoint defined successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ULTIMATE MEM0 SYSTEM TEST STARTING...")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Redis Connection Test", test_redis_connection),
        ("Mem0 Client Test", test_mem0_client),
        ("Flask App Test", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🔥 ALL TESTS PASSED! ULTIMATE MEM0 SYSTEM READY!")
        print("🚀 Ready to deploy to Railway!")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)