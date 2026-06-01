# 🚀 Quick Start Guide

## Get Your Model Deployed in 5 Minutes!

### Step 1: Export Models (2 minutes)

1. Open your Jupyter notebook: `23f2000680-notebook-t12026 (2).ipynb`

2. Add this cell at the very end and run it:

```python
import joblib
import os

os.makedirs('models', exist_ok=True)

# Save all models
joblib.dump(lgb_model, 'models/lgb_model.pkl')
joblib.dump(xgb_model, 'models/xgb_model.pkl')
joblib.dump(lr_model, 'models/lr_model.pkl')
joblib.dump(nb_model, 'models/nb_model.pkl')

# Save preprocessors
joblib.dump(tfidf_word, 'models/tfidf_word.pkl')
joblib.dump(tfidf_char, 'models/tfidf_char.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

# Save feature names
feature_names = ['emoticon_1', 'emoticon_2', 'emoticon_3',
                 'upvote', 'downvote', 'if_1', 'if_2',
                 'comment_length', 'word_count']
joblib.dump(feature_names, 'models/feature_names.pkl')

print('✅ Models exported! Run: python app.py')
```

### Step 2: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 3: Start the Server (30 seconds)

```bash
python app.py
```

You should see:
```
✓ All models and preprocessors loaded successfully
Starting Flask server...
 * Running on http://0.0.0.0:5000
```

### Step 4: Test It! (1 minute)

Open a new terminal and run:

```bash
python test_api.py
```

Or test with curl:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "This is amazing!",
    "emoticon_1": 1,
    "emoticon_2": 0,
    "emoticon_3": 0,
    "upvote": 10,
    "downvote": 0,
    "if_1": 0,
    "if_2": 5
  }'
```

Expected response:
```json
{
  "prediction": 1,
  "category": "Positive",
  "confidence": 0.85,
  "probabilities": {
    "class_0": 0.05,
    "class_1": 0.85,
    "class_2": 0.10
  }
}
```

## 🎉 That's It!

Your model is now running as a REST API!

## 📱 What Can You Do Now?

### Use it in your applications:

**Python:**
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    "comment": "Great work!",
    "emoticon_1": 1,
    "emoticon_2": 0,
    "emoticon_3": 0,
    "upvote": 5,
    "downvote": 0,
    "if_1": 0,
    "if_2": 10
})

print(response.json())
```

**JavaScript:**
```javascript
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    comment: "Great work!",
    emoticon_1: 1,
    emoticon_2: 0,
    emoticon_3: 0,
    upvote: 5,
    downvote: 0,
    if_1: 0,
    if_2: 10
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

**cURL:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"comment":"Great!","emoticon_1":1,"emoticon_2":0,"emoticon_3":0,"upvote":5,"downvote":0,"if_1":0,"if_2":10}'
```

## 🌐 Deploy to the Cloud

### Heroku (Easiest)
```bash
heroku create
git init
git add .
git commit -m "Deploy"
git push heroku main
```

### Docker
```bash
docker build -t comment-predictor .
docker run -p 5000:5000 comment-predictor
```

### Google Cloud Run
```bash
gcloud run deploy --source . --platform managed
```

## 📚 Need More Help?

- Full documentation: `README.md`
- Deployment checklist: `DEPLOYMENT_CHECKLIST.md`
- Export instructions: `EXPORT_MODELS_CELL.md`

## ❓ Troubleshooting

**Models not loading?**
- Make sure you ran the export cell in your notebook
- Check that `models/` directory has 8 `.pkl` files

**Port 5000 in use?**
```bash
# Kill the process
lsof -ti:5000 | xargs kill -9
```

**Import errors?**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

Happy deploying! 🚀
