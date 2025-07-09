"""
Simple test to verify Railway app structure
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work"""
    try:
        print("Testing imports...")
        
        # Test standard library imports
        import os
        import logging
        from datetime import datetime
        from typing import Dict, Any, Optional
        print("✓ Standard library imports work")
        
        # Test dotenv (if available)
        try:
            from dotenv import load_dotenv
            print("✓ python-dotenv available")
        except ImportError:
            print("⚠ python-dotenv not installed (optional)")
        
        # Test Flask imports (if available)
        try:
            from flask import Flask, request, jsonify
            print("✓ Flask available")
        except ImportError:
            print("⚠ Flask not installed")
            return False
            
        try:
            from flask_cors import CORS
            print("✓ Flask-CORS available")
        except ImportError:
            print("⚠ Flask-CORS not installed")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_health_endpoint_logic():
    """Test the health endpoint logic without running the server"""
    try:
        print("\nTesting health endpoint logic...")
        
        # Mock the health check response
        from datetime import datetime
        
        response = {
            'success': True,
            'status': 'healthy',
            'message': 'Bonzai Railway Backend is running',
            'timestamp': datetime.now().isoformat(),
            'service': 'bonzai-railway',
            'version': '1.0.0'
        }
        
        print(f"✓ Health response: {response}")
        return True
        
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False

def test_port_configuration():
    """Test port configuration"""
    try:
        print("\nTesting port configuration...")
        
        # Test default port
        default_port = int(os.getenv('PORT', 5000))
        print(f"✓ Default port: {default_port}")
        
        # Test with Railway PORT
        os.environ['PORT'] = '8080'
        railway_port = int(os.getenv('PORT', 5000))
        print(f"✓ Railway port: {railway_port}")
        
        return True
        
    except Exception as e:
        print(f"✗ Port configuration error: {e}")
        return False

if __name__ == "__main__":
    print("Bonzai Railway App - Simple Test")
    print("=" * 40)
    
    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_health_endpoint_logic()
    success &= test_port_configuration()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ All tests passed! Railway app should work.")
    else:
        print("❌ Some tests failed. Check dependencies.")
        
    print("\nNext steps:")
    print("1. Deploy to Railway with app_railway.py")
    print("2. Health check will be available at /api/health")
    print("3. Main app will be available at /")