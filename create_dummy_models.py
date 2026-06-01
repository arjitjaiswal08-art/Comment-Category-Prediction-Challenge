"""
Create dummy models for testing deployment
This allows you to test the deployment before training the actual models
"""

import joblib
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

print("=" * 60)
print("CREATING DUMMY MODELS FOR TESTING")
print("=" * 60)
print("\n⚠️  WARNING: These are DUMMY models for testing only!")
print("Replace them with your actual trained models from the notebook.\n")

# Create models directory
os.makedirs('models', exist_ok=True)

# Create dummy model objects (simple dictionaries that mimic model behavior)
class DummyModel:
    def predict(self, X):
        # Return random predictions for 3 classes
        n_samples = X.shape[0]
        return np.random.rand(n_samples, 3)
    
    def predict_proba(self, X):
        return self.predict(X)

# Create and save dummy models
print("Creating dummy models...")
lgb_model = DummyModel()
xgb_model = DummyModel()
lr_model = DummyModel()
nb_model = DummyModel()

joblib.dump(lgb_model, 'models/lgb_model.pkl')
print("✓ LightGBM dummy model created")

joblib.dump(xgb_model, 'models/xgb_model.pkl')
print("✓ XGBoost dummy model created")

joblib.dump(lr_model, 'models/lr_model.pkl')
print("✓ Logistic Regression dummy model created")

joblib.dump(nb_model, 'models/nb_model.pkl')
print("✓ Naive Bayes dummy model created")

# Create dummy preprocessors
print("\nCreating dummy preprocessors...")

# TF-IDF vectorizers
tfidf_word = TfidfVectorizer(max_features=100)
tfidf_char = TfidfVectorizer(max_features=50, analyzer='char', ngram_range=(2, 4))

# Fit on dummy data
dummy_texts = ["sample text", "another sample", "test comment"]
tfidf_word.fit(dummy_texts)
tfidf_char.fit(dummy_texts)

joblib.dump(tfidf_word, 'models/tfidf_word.pkl')
print("✓ TF-IDF Word vectorizer created")

joblib.dump(tfidf_char, 'models/tfidf_char.pkl')
print("✓ TF-IDF Char vectorizer created")

# Scaler
scaler = StandardScaler()
dummy_features = np.random.rand(10, 9)  # 9 numerical features
scaler.fit(dummy_features)

joblib.dump(scaler, 'models/scaler.pkl')
print("✓ StandardScaler created")

# Feature names
feature_names = ['emoticon_1', 'emoticon_2', 'emoticon_3',
                 'upvote', 'downvote', 'if_1', 'if_2',
                 'comment_length', 'word_count']
joblib.dump(feature_names, 'models/feature_names.pkl')
print("✓ Feature names saved")

print("\n" + "=" * 60)
print("✅ DUMMY MODELS CREATED SUCCESSFULLY!")
print("=" * 60)

print("\n📁 Files created in models/ directory:")
for filename in os.listdir('models'):
    filepath = os.path.join('models', filename)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  {filename}: {size_kb:.2f} KB")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("\n1. Push to GitHub:")
print("   git add models/")
print("   git commit -m 'Add dummy models for testing'")
print("   git push origin main")
print("\n2. Deploy on Render.com (it will work now!)")
print("\n3. Later, replace with real models:")
print("   - Train your models in the notebook")
print("   - Export them using the code in EXPORT_MODELS_CELL.md")
print("   - Push the real models to GitHub")
print("   - Render will auto-deploy!")
print("\n" + "=" * 60)
