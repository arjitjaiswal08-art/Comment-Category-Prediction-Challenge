# Comment Category Prediction Model - Deployment Guide

This is a production-ready deployment setup for the comment category prediction ensemble model trained in the Jupyter notebook.

## 📋 Overview

The model predicts comment categories using an ensemble of:
- **LightGBM** (35% weight)
- **XGBoost** (35% weight)
- **Logistic Regression** (20% weight)
- **Naive Bayes** (10% weight)

## 🚀 Quick Start

### Step 1: Export Models from Notebook

Open your Jupyter notebook and add this cell at the end (after training all models):

```python
import joblib
import os

# Create models directory
os.makedirs('models', exist_ok=True)

# Save models
print("Saving models...")
joblib.dump(lgb_model, 'models/lgb_model.pkl')
joblib.dump(xgb_model, 'models/xgb_model.pkl')
joblib.dump(lr_model, 'models/lr_model.pkl')
joblib.dump(nb_model, 'models/nb_model.pkl')

# Save preprocessors
print("Saving preprocessors...")
joblib.dump(tfidf_word, 'models/tfidf_word.pkl')
joblib.dump(tfidf_char, 'models/tfidf_char.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

# Save feature names
feature_names = ['emoticon_1', 'emoticon_2', 'emoticon_3',
                 'upvote', 'downvote', 'if_1', 'if_2',
                 'comment_length', 'word_count']
joblib.dump(feature_names, 'models/feature_names.pkl')

print('✓ All models exported successfully!')
print('✓ You can now run: python app.py')
```

Run this cell, and all models will be saved to the `models/` directory.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start the API Server

```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

The API will be available at `http://localhost:5000`

### Step 4: Test the API

```bash
python test_api.py
```

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

### 2. Single Prediction
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "comment": "This is a great article!",
  "emoticon_1": 1,
  "emoticon_2": 0,
  "emoticon_3": 0,
  "upvote": 5,
  "downvote": 0,
  "if_1": 0,
  "if_2": 10
}
```

**Response:**
```json
{
  "prediction": 1,
  "category": "Positive",
  "confidence": 0.87,
  "probabilities": {
    "class_0": 0.05,
    "class_1": 0.87,
    "class_2": 0.08
  }
}
```

### 3. Batch Prediction
```http
POST /batch_predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "comments": [
    {
      "comment": "Great content!",
      "emoticon_1": 1,
      "emoticon_2": 0,
      "emoticon_3": 0,
      "upvote": 10,
      "downvote": 0,
      "if_1": 0,
      "if_2": 5
    },
    {
      "comment": "Disappointing...",
      "emoticon_1": 0,
      "emoticon_2": 0,
      "emoticon_3": 1,
      "upvote": 0,
      "downvote": 5,
      "if_1": 0,
      "if_2": 10
    }
  ]
}
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t comment-predictor .
```

### Run Container
```bash
docker run -p 5000:5000 comment-predictor
```

### Docker Compose (Optional)
Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment Options

### Option 1: AWS (Elastic Beanstalk or ECS)
1. Package your application
2. Create an Elastic Beanstalk environment
3. Deploy using EB CLI or AWS Console

### Option 2: Google Cloud Platform (Cloud Run)
```bash
gcloud run deploy comment-predictor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: Azure (App Service)
```bash
az webapp up --name comment-predictor \
  --resource-group myResourceGroup \
  --runtime "PYTHON:3.10"
```

### Option 4: Heroku
```bash
heroku create comment-predictor
git push heroku main
```

### Option 5: Railway, Render, or Fly.io
These platforms support direct deployment from GitHub with automatic Docker detection.

## 📊 Model Performance

Based on the notebook training:
- **Training Accuracy**: ~XX%
- **Validation Accuracy**: ~XX%
- **F1 Score**: ~XX

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```bash
FLASK_ENV=production
WORKERS=4
TIMEOUT=120
PORT=5000
```

### Model Weights
Adjust ensemble weights in `app.py`:

```python
ensemble_proba = (
    0.35 * lgb_proba +   # LightGBM weight
    0.35 * xgb_proba +   # XGBoost weight
    0.20 * lr_proba +    # Logistic Regression weight
    0.10 * nb_proba      # Naive Bayes weight
)
```

## 📁 Project Structure

```
mlp_d/
├── app.py                  # Flask API application
├── export_models.py        # Model export helper script
├── test_api.py            # API testing script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── README.md              # This file
├── models/                # Exported models (created after export)
│   ├── lgb_model.pkl
│   ├── xgb_model.pkl
│   ├── lr_model.pkl
│   ├── nb_model.pkl
│   ├── tfidf_word.pkl
│   ├── tfidf_char.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
└── 23f2000680-notebook-t12026 (2).ipynb  # Original notebook
```

## 🐛 Troubleshooting

### Models not loading
- Make sure you've run the export code in your notebook
- Check that the `models/` directory contains all `.pkl` files
- Verify file permissions

### Port already in use
```bash
# Change port in app.py or use:
python app.py --port 5001
```

### Memory issues
- Reduce number of workers in Gunicorn
- Increase Docker container memory limit
- Use a larger cloud instance

## 📈 Monitoring & Logging

Add logging to `app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

## 🔒 Security Considerations

- Add API authentication (JWT tokens, API keys)
- Enable HTTPS in production
- Add rate limiting
- Input validation and sanitization
- CORS configuration if needed

## 📝 License

[Add your license here]

## 👥 Contributors

[Add contributors here]

## 📧 Contact

For questions or issues, please contact [your email/contact info]
