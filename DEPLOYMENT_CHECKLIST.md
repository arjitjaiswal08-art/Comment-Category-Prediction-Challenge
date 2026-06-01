# 🚀 Deployment Checklist

## ✅ Pre-Deployment Steps

### 1. Export Models from Notebook
- [ ] Open your Jupyter notebook: `23f2000680-notebook-t12026 (2).ipynb`
- [ ] Run all cells to train the models
- [ ] Add and run the export cell from `EXPORT_MODELS_CELL.md`
- [ ] Verify `models/` directory contains 8 `.pkl` files:
  - `lgb_model.pkl`
  - `xgb_model.pkl`
  - `lr_model.pkl`
  - `nb_model.pkl`
  - `tfidf_word.pkl`
  - `tfidf_char.pkl`
  - `scaler.pkl`
  - `feature_names.pkl`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

- [ ] All packages installed successfully
- [ ] No version conflicts

### 3. Test Locally

#### Start the server:
```bash
python app.py
```

- [ ] Server starts without errors
- [ ] Models load successfully
- [ ] Server running on http://localhost:5000

#### Run tests (in a new terminal):
```bash
python test_api.py
```

- [ ] Health check passes
- [ ] Single prediction works
- [ ] Batch prediction works

#### Manual test with curl:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "This is a test comment",
    "emoticon_1": 0,
    "emoticon_2": 0,
    "emoticon_3": 0,
    "upvote": 5,
    "downvote": 0,
    "if_1": 0,
    "if_2": 10
  }'
```

- [ ] Returns valid JSON response
- [ ] Prediction makes sense

## 🐳 Docker Deployment (Optional)

### Build and Test Docker Image
```bash
docker build -t comment-predictor .
docker run -p 5000:5000 comment-predictor
```

- [ ] Docker image builds successfully
- [ ] Container starts without errors
- [ ] API accessible at http://localhost:5000
- [ ] Health check passes

## ☁️ Cloud Deployment Options

### Option A: Heroku

1. Create Heroku app:
```bash
heroku create your-app-name
```

2. Add `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
```

3. Deploy:
```bash
git init
git add .
git commit -m "Initial deployment"
git push heroku main
```

4. Check:
```bash
heroku logs --tail
```

- [ ] App deployed successfully
- [ ] Logs show no errors
- [ ] Health endpoint accessible

### Option B: Google Cloud Run

```bash
gcloud run deploy comment-predictor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

- [ ] Service deployed
- [ ] Health check passes
- [ ] API responds correctly

### Option C: AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize and deploy:
```bash
eb init -p python-3.10 comment-predictor
eb create comment-predictor-env
eb open
```

- [ ] Environment created
- [ ] Application healthy
- [ ] API accessible

### Option D: Azure App Service

```bash
az webapp up \
  --name comment-predictor \
  --resource-group myResourceGroup \
  --runtime "PYTHON:3.10" \
  --sku B1
```

- [ ] App service created
- [ ] Deployment successful
- [ ] API responds correctly

### Option E: Railway / Render / Fly.io

1. Connect GitHub repository
2. Select Python runtime
3. Deploy automatically

- [ ] Auto-deployment configured
- [ ] Build successful
- [ ] Service running

## 📊 Post-Deployment Verification

### Test Production Endpoint
Replace `YOUR_URL` with your deployed URL:

```bash
# Health check
curl https://YOUR_URL/health

# Single prediction
curl -X POST https://YOUR_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Great article!",
    "emoticon_1": 1,
    "emoticon_2": 0,
    "emoticon_3": 0,
    "upvote": 10,
    "downvote": 0,
    "if_1": 0,
    "if_2": 5
  }'
```

- [ ] Health endpoint returns 200
- [ ] Prediction endpoint returns valid results
- [ ] Response time acceptable (< 2 seconds)

### Load Testing (Optional)
```bash
# Install apache bench
sudo apt-get install apache-bench

# Run load test
ab -n 100 -c 10 https://YOUR_URL/health
```

- [ ] Server handles concurrent requests
- [ ] No errors under load
- [ ] Response times consistent

## 🔒 Security Checklist

- [ ] API keys/authentication added (if needed)
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Input validation in place
- [ ] Error messages don't expose sensitive info
- [ ] CORS configured properly
- [ ] Environment variables secured

## 📈 Monitoring Setup

- [ ] Logging configured
- [ ] Error tracking (Sentry, etc.)
- [ ] Performance monitoring
- [ ] Uptime monitoring
- [ ] Alert notifications set up

## 📝 Documentation

- [ ] API documentation complete
- [ ] Example requests/responses documented
- [ ] Error codes documented
- [ ] Rate limits specified
- [ ] Contact information provided

## 🎉 Final Steps

- [ ] Share API endpoint with team
- [ ] Add to project documentation
- [ ] Set up CI/CD pipeline (if needed)
- [ ] Plan for model updates
- [ ] Schedule regular monitoring checks

---

## Common Issues & Solutions

### Issue: Models not loading
**Solution**: Verify all 8 .pkl files exist in models/ directory

### Issue: Port already in use
**Solution**: Kill existing process or change port
```bash
lsof -ti:5000 | xargs kill -9
```

### Issue: Memory errors
**Solution**: Reduce workers or increase instance memory
```bash
gunicorn --workers 2 --timeout 120 app:app
```

### Issue: Slow predictions
**Solution**: 
- Enable model caching
- Use batch predictions
- Increase worker count
- Upgrade instance

---

## Support

If you encounter issues:
1. Check server logs
2. Verify model files
3. Test locally first
4. Check cloud service status
5. Review error messages carefully

Good luck with your deployment! 🚀
