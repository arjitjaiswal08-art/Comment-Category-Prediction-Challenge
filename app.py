"""
Flask API for Comment Category Prediction Model
Serves predictions from the ensemble model trained in the notebook
"""

from flask import Flask, request, jsonify, render_template_string
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
import re
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comment Category Prediction</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 120px;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 12px;
            display: none;
        }
        
        .result.show {
            display: block;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .result.positive {
            background: #d4edda;
            border: 2px solid #28a745;
        }
        
        .result.negative {
            background: #f8d7da;
            border: 2px solid #dc3545;
        }
        
        .result.neutral {
            background: #d1ecf1;
            border: 2px solid #17a2b8;
        }
        
        .result-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .result.positive .result-title {
            color: #28a745;
        }
        
        .result.negative .result-title {
            color: #dc3545;
        }
        
        .result.neutral .result-title {
            color: #17a2b8;
        }
        
        .confidence {
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
        }
        
        .probabilities {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .prob-item {
            flex: 1;
            min-width: 100px;
            padding: 10px;
            background: rgba(255,255,255,0.7);
            border-radius: 8px;
            text-align: center;
        }
        
        .prob-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .prob-value {
            font-size: 18px;
            font-weight: 600;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #f8d7da;
            border: 2px solid #dc3545;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        
        .error.show {
            display: block;
        }
        
        .example-comments {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .example-title {
            font-size: 14px;
            font-weight: 600;
            color: #555;
            margin-bottom: 10px;
        }
        
        .example-item {
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 13px;
            color: #666;
            transition: background 0.2s;
        }
        
        .example-item:hover {
            background: #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 Comment Category Prediction</h1>
        <p class="subtitle">Analyze comment sentiment using AI</p>
        
        <form id="predictionForm">
            <div class="form-group">
                <label for="comment">Enter your comment:</label>
                <textarea 
                    id="comment" 
                    name="comment" 
                    placeholder="Type your comment here..."
                    required
                ></textarea>
            </div>
            
            <div class="features-grid">
                <div class="form-group">
                    <label for="emoticon_1">😊 Emoticon 1:</label>
                    <input type="number" id="emoticon_1" name="emoticon_1" value="0" min="0">
                </div>
                <div class="form-group">
                    <label for="emoticon_2">😐 Emoticon 2:</label>
                    <input type="number" id="emoticon_2" name="emoticon_2" value="0" min="0">
                </div>
                <div class="form-group">
                    <label for="emoticon_3">😢 Emoticon 3:</label>
                    <input type="number" id="emoticon_3" name="emoticon_3" value="0" min="0">
                </div>
                <div class="form-group">
                    <label for="upvote">👍 Upvotes:</label>
                    <input type="number" id="upvote" name="upvote" value="0" min="0">
                </div>
                <div class="form-group">
                    <label for="downvote">👎 Downvotes:</label>
                    <input type="number" id="downvote" name="downvote" value="0" min="0">
                </div>
                <div class="form-group">
                    <label for="if_1">IF 1:</label>
                    <input type="number" id="if_1" name="if_1" value="0" min="0">
                </div>
                <div class="form-group">
                    <label for="if_2">IF 2:</label>
                    <input type="number" id="if_2" name="if_2" value="10" min="0">
                </div>
            </div>
            
            <button type="submit" id="submitBtn">Analyze Comment</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 10px; color: #666;">Analyzing...</p>
        </div>
        
        <div class="result" id="result">
            <div class="result-title" id="resultTitle"></div>
            <div class="confidence" id="confidence"></div>
            <div class="probabilities">
                <div class="prob-item">
                    <div class="prob-label">Neutral</div>
                    <div class="prob-value" id="prob0">0%</div>
                </div>
                <div class="prob-item">
                    <div class="prob-label">Positive</div>
                    <div class="prob-value" id="prob1">0%</div>
                </div>
                <div class="prob-item">
                    <div class="prob-label">Negative</div>
                    <div class="prob-value" id="prob2">0%</div>
                </div>
            </div>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="example-comments">
            <div class="example-title">Try these examples:</div>
            <div class="example-item" onclick="fillExample('This is amazing! Great work!')">
                "This is amazing! Great work!"
            </div>
            <div class="example-item" onclick="fillExample('This is terrible and disappointing.')">
                "This is terrible and disappointing."
            </div>
            <div class="example-item" onclick="fillExample('It is what it is.')">
                "It is what it is."
            </div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('predictionForm');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const error = document.getElementById('error');
        const submitBtn = document.getElementById('submitBtn');
        
        function fillExample(text) {
            document.getElementById('comment').value = text;
        }
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Hide previous results
            result.classList.remove('show');
            error.classList.remove('show');
            loading.classList.add('show');
            submitBtn.disabled = true;
            
            // Get form data
            const formData = {
                comment: document.getElementById('comment').value,
                emoticon_1: parseInt(document.getElementById('emoticon_1').value),
                emoticon_2: parseInt(document.getElementById('emoticon_2').value),
                emoticon_3: parseInt(document.getElementById('emoticon_3').value),
                upvote: parseInt(document.getElementById('upvote').value),
                downvote: parseInt(document.getElementById('downvote').value),
                if_1: parseInt(document.getElementById('if_1').value),
                if_2: parseInt(document.getElementById('if_2').value)
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Show result
                    const categories = ['neutral', 'positive', 'negative'];
                    const category = categories[data.prediction];
                    
                    result.className = 'result show ' + category;
                    document.getElementById('resultTitle').textContent = 
                        '📊 Prediction: ' + data.category;
                    document.getElementById('confidence').textContent = 
                        'Confidence: ' + (data.confidence * 100).toFixed(1) + '%';
                    
                    document.getElementById('prob0').textContent = 
                        (data.probabilities.class_0 * 100).toFixed(1) + '%';
                    document.getElementById('prob1').textContent = 
                        (data.probabilities.class_1 * 100).toFixed(1) + '%';
                    document.getElementById('prob2').textContent = 
                        (data.probabilities.class_2 * 100).toFixed(1) + '%';
                } else {
                    throw new Error(data.error || 'Prediction failed');
                }
            } catch (err) {
                error.textContent = '❌ Error: ' + err.message;
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

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
    """Home page with web interface"""
    return render_template_string(HTML_TEMPLATE)

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
