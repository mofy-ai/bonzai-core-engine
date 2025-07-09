# Railway Deployment Guide for Bonzai Backend

## Problem Analysis

The original `app.py` was failing Railway health checks because:

1. **Complex Service Initialization**: Trying to load 16+ services at startup
2. **Import Failures**: Missing dependencies causing startup failures
3. **Async/Sync Issues**: Improper mixing of async and sync operations
4. **Port Configuration**: Not using Railway's PORT environment variable
5. **Service Dependencies**: Many services had import errors preventing startup

## Solution

Created streamlined versions that focus on getting the app running first, then adding features.

## Quick Fix (Recommended)

### Option 1: Minimal Deployment

Use the ultra-minimal version that's guaranteed to work:

```bash
# 1. Replace your current files
cp Procfile.minimal Procfile
cp requirements_minimal.txt requirements.txt
cp railway_minimal.json railway.json

# 2. Deploy to Railway
# The app will start with app_railway_minimal.py
```

### Option 2: Standard Deployment

Use the standard Railway-optimized version:

```bash
# 1. Replace your current files
cp Procfile.gunicorn Procfile  # Use Gunicorn for production
cp requirements_railway_minimal.txt requirements.txt
# Keep railway.json as is

# 2. Deploy to Railway
# The app will start with app_railway.py using Gunicorn
```

## Files Created

### Core Application Files

1. **`app_railway_minimal.py`** - Ultra-minimal version (guaranteed to work)
   - Only Flask + health endpoint
   - Manual CORS handling
   - Minimal dependencies

2. **`app_railway.py`** - Standard Railway version
   - Basic services + health endpoint
   - Flask-CORS integration
   - More features but more dependencies

3. **`gunicorn.conf.py`** - Production server configuration
   - Optimized for Railway
   - Single worker to start
   - Proper logging

### Deployment Files

1. **`Procfile.minimal`** - For minimal deployment
2. **`Procfile.gunicorn`** - For production deployment
3. **`railway_minimal.json`** - Minimal Railway configuration
4. **`requirements_minimal.txt`** - Ultra-minimal dependencies

## Health Check Endpoints

All versions include the critical health check endpoint:

```
GET /api/health
```

Response:
```json
{
  "success": true,
  "status": "healthy",
  "message": "Bonzai Railway Backend is running",
  "timestamp": "2025-07-09T13:20:17.999385",
  "service": "bonzai-railway",
  "version": "1.0.0"
}
```

## Port Configuration

All versions properly handle Railway's PORT environment variable:

```python
port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

## Testing

Test files are provided to verify functionality:

```bash
# Test minimal version
python3 test_minimal.py

# Test standard version
python3 test_railway_simple.py
```

## Deployment Steps

### Step 1: Choose Your Version

**For immediate fix (recommended):**
```bash
cp Procfile.minimal Procfile
cp requirements_minimal.txt requirements.txt
cp railway_minimal.json railway.json
```

**For production deployment:**
```bash
cp Procfile.gunicorn Procfile
cp requirements_railway_minimal.txt requirements.txt
# railway.json is already configured
```

### Step 2: Commit and Deploy

```bash
git add .
git commit -m "Fix Railway health checks with streamlined deployment"
git push origin main
```

### Step 3: Verify Health Check

Once deployed, test the health check:
```bash
curl https://your-app.railway.app/api/health
```

## Expected Results

✅ **Health check passes within 60 seconds**
✅ **App starts successfully**
✅ **No import errors**
✅ **Proper port binding**
✅ **Basic CORS support**

## Next Steps

Once the basic deployment works:

1. **Add API Keys**: Set environment variables in Railway for API keys
2. **Add Services**: Gradually add back the services from the original app.py
3. **Add Features**: Implement the AI models and other features
4. **Scale Up**: Use more Gunicorn workers as needed

## Environment Variables

Set these in Railway dashboard:

```env
SECRET_KEY=your-secret-key
MEM0_API_KEY=your-mem0-key
GEMINI_API_KEY_PRIMARY=your-gemini-key
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
```

## Troubleshooting

**If health check still fails:**
1. Check Railway logs for startup errors
2. Verify PORT environment variable is set
3. Ensure requirements.txt has correct dependencies
4. Test locally with `python3 app_railway_minimal.py`

**If you get import errors:**
1. Use the minimal version first
2. Add dependencies one by one
3. Check for typos in requirements.txt

## File Structure

```
bonzai-core-engine/
├── app_railway_minimal.py     # Ultra-minimal version
├── app_railway.py             # Standard version
├── Procfile.minimal           # Minimal Procfile
├── Procfile.gunicorn          # Production Procfile
├── requirements_minimal.txt   # Minimal dependencies
├── requirements_railway_minimal.txt  # Railway dependencies
├── railway_minimal.json       # Minimal Railway config
├── gunicorn.conf.py          # Gunicorn configuration
└── test_minimal.py           # Test script
```

## Success Metrics

- ✅ Railway health check passes
- ✅ App starts in under 60 seconds
- ✅ `/api/health` returns 200 OK
- ✅ Basic functionality works
- ✅ No startup errors in logs