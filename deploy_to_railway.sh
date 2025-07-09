#!/bin/bash

echo "🚀 Bonzai Railway Deployment Script"
echo "======================================"

# Function to deploy minimal version
deploy_minimal() {
    echo "📦 Deploying MINIMAL version..."
    
    # Backup original files
    cp Procfile Procfile.backup 2>/dev/null || true
    cp requirements.txt requirements.txt.backup 2>/dev/null || true
    cp railway.json railway.json.backup 2>/dev/null || true
    
    # Deploy minimal files
    cp Procfile.minimal Procfile
    cp requirements_minimal.txt requirements.txt
    cp railway_minimal.json railway.json
    
    echo "✅ Minimal deployment files configured"
    echo "   - App: app_railway_minimal.py"
    echo "   - Dependencies: flask, python-dotenv"
    echo "   - Health check timeout: 60s"
}

# Function to deploy standard version
deploy_standard() {
    echo "📦 Deploying STANDARD version..."
    
    # Backup original files
    cp Procfile Procfile.backup 2>/dev/null || true
    cp requirements.txt requirements.txt.backup 2>/dev/null || true
    
    # Deploy standard files
    cp Procfile.gunicorn Procfile
    cp requirements_railway_minimal.txt requirements.txt
    # Keep existing railway.json
    
    echo "✅ Standard deployment files configured"
    echo "   - App: app_railway.py with Gunicorn"
    echo "   - Dependencies: flask, flask-cors, gunicorn"
    echo "   - Health check timeout: 120s"
}

# Function to test deployment
test_deployment() {
    echo "🧪 Testing deployment..."
    
    if [ -f "test_minimal.py" ]; then
        python3 test_minimal.py
    else
        echo "⚠️  Test file not found, skipping tests"
    fi
}

# Main menu
echo ""
echo "Choose deployment option:"
echo "1. Minimal (recommended for quick fix)"
echo "2. Standard (for production)"
echo "3. Test only"
echo "4. Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        deploy_minimal
        test_deployment
        ;;
    2)
        deploy_standard
        test_deployment
        ;;
    3)
        test_deployment
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run again."
        exit 1
        ;;
esac

echo ""
echo "🎯 Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Fix Railway health checks'"
echo "2. Push to deploy: git push origin main"
echo "3. Check Railway logs for deployment status"
echo "4. Test health check: curl https://your-app.railway.app/api/health"
echo ""
echo "🔧 If issues persist, check Railway logs and verify environment variables"