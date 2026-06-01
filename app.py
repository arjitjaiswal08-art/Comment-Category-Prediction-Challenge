"""
Flask API for Comment Category Prediction Model
Serves predictions from the ensemble model trained in the notebook
"""

from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
import re
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Global variables for models and preprocessors
models = {}
preprocessors = {}

def load_models():
    """Load all trained models and preprocessors"""
    global models, preprocessors
    
    try:
        # Load models
        models['lgb'] = joblib.load('models/lgb_model.pkl')
        models['xgb'] = joblib.load('models/xgb_model.pkl')
        models['lr'] = joblib.load('models/lr_model.pkl')
        models['nb'] = joblib.load('models/nb_model.pkl')
        
        # Load preprocessors
        preprocessors['tfidf_word'] = joblib.load('models/tfidf_word.pkl')
        preprocessors['tfidf_char'] = joblib.load('models/tfidf_char.pkl')
        preprocessors['scaler'] = joblib.load('models/scaler.pkl')
        preprocessors['feature_names'] = joblib.load('models/feature_names.pkl')
        
        print("✓ All models and preprocessors loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Error loading models: {str(e)}")
        return False

def preprocess_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_features(data):
    """Extract features from input data"""
    df = pd.DataFrame([data])
    
    # Preprocess comment
    df['comment_clean'] = df['comment'].apply(preprocess_text)
    df['comment_length'] = df['comment_clean'].str.len()
    df['word_count'] = df['comment_clean'].str.split().str.len()
    
    # TF-IDF features
    tfidf_word_features = preprocessors['tfidf_word'].transform(df['comment_clean'])
    tfidf_char_features = preprocessors['tfidf_char'].transform(df['comment_clean'])
    
    # Numerical features
    numerical_cols = ['emoticon_1', 'emoticon_2', 'emoticon_3', 'upvote', 
                     'downvote', 'if_1', 'if_2', 'comment_length', 'word_count']
    
    numerical_features = df[numerical_cols].fillna(0).values
    numerical_features_scaled = preprocessors['scaler'].transform(numerical_features)
    
    # Combine all features
    X = hstack([
        tfidf_word_features,
        tfidf_char_features,
        csr_matrix(numerical_features_scaled)
    ])
    
    return X, tfidf_word_features, tfidf_char_features

def predict_ensemble(X, X_tfidf_word, X_tfidf_char):
    """Make ensemble prediction"""
    # Get predictions from all models
    lgb_proba = models['lgb'].predict(X)
    
    import xgboost as xgb
    dmatrix = xgb.DMatrix(X)
    xgb_proba = models['xgb'].predict(dmatrix)
    
    lr_proba = models['lr'].predict_proba(X)
    
    # NB uses only TF-IDF features
    X_nb = hstack([X_tfidf_word, X_tfidf_char])
    nb_proba = models['nb'].predict_proba(X_nb)
    
    # Ensemble with weights
    ensemble_proba = (
        0.35 * lgb_proba +
        0.35 * xgb_proba +
        0.20 * lr_proba +
        0.10 * nb_proba
    )
    
    prediction = ensemble_proba.argmax(axis=1)[0]
    confidence = ensemble_proba.max(axis=1)[0]
    
    return int(prediction), float(confidence), ensemble_proba[0].tolist()

@app.route('/', methods=['GET'])
def home():
    """Home page"""
    return jsonify({
        'message': 'Comment Category Prediction API',
        'version': '1.0',
        'endpoints': {
            'health': '/health',
            'predict': '/predict (POST)',
            'batch_predict': '/batch_predict (POST)'
        },
        'status': 'running'
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(models) == 4
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['comment', 'emoticon_1', 'emoticon_2', 'emoticon_3',
                          'upvote', 'downvote', 'if_1', 'if_2']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract features
        X, X_tfidf_word, X_tfidf_char = extract_features(data)
        
        # Make prediction
        prediction, confidence, probabilities = predict_ensemble(X, X_tfidf_word, X_tfidf_char)
        
        # Category mapping
        category_map = {
            0: 'Neutral',
            1: 'Positive',
            2: 'Negative'
        }
        
        return jsonify({
            'prediction': prediction,
            'category': category_map.get(prediction, 'Unknown'),
            'confidence': confidence,
            'probabilities': {
                'class_0': probabilities[0],
                'class_1': probabilities[1],
                'class_2': probabilities[2]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint"""
    try:
        data = request.get_json()
        
        if 'comments' not in data or not isinstance(data['comments'], list):
            return jsonify({'error': 'Expected "comments" list in request body'}), 400
        
        results = []
        for item in data['comments']:
            X, X_tfidf_word, X_tfidf_char = extract_features(item)
            prediction, confidence, probabilities = predict_ensemble(X, X_tfidf_word, X_tfidf_char)
            
            results.append({
                'prediction': prediction,
                'confidence': confidence,
                'probabilities': probabilities
            })
        
        return jsonify({'predictions': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Loading models...")
    if load_models():
        print("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Failed to load models. Please run export_models.py first.")
