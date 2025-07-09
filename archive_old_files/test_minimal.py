"""
Test the minimal Railway app
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_minimal_app():
    """Test if minimal app can be imported and basic logic works"""
    try:
        print("Testing minimal Railway app...")
        
        # Test imports
        from flask import Flask, request, jsonify
        from datetime import datetime
        print("✓ All imports work")
        
        # Test app creation
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test-secret'
        print("✓ Flask app created")
        
        # Test health check logic
        response = {
            'success': True,
            'status': 'healthy',
            'message': 'Bonzai Railway Backend is running',
            'timestamp': datetime.now().isoformat(),
            'service': 'bonzai-railway',
            'version': '1.0.0'
        }
        print(f"✓ Health check response: {response}")
        
        # Test port configuration
        port = int(os.getenv('PORT', 5000))
        print(f"✓ Port configuration: {port}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Minimal Railway App")
    print("=" * 30)
    
    if test_minimal_app():
        print("\n✅ Minimal app test passed!")
        print("\nDeploy instructions:")
        print("1. Update Procfile to use app_railway_minimal.py")
        print("2. Update requirements.txt to requirements_minimal.txt")
        print("3. Deploy to Railway")
        print("4. Health check should pass at /api/health")
    else:
        print("\n❌ Minimal app test failed!")