# Add This Cell to Your Notebook

Copy and paste this code into a new cell at the end of your Jupyter notebook (after all models are trained):

```python
# ============================================================
# EXPORT MODELS FOR DEPLOYMENT
# ============================================================

import joblib
import os

# Create models directory
os.makedirs('models', exist_ok=True)

print("=" * 60)
print("EXPORTING MODELS FOR DEPLOYMENT")
print("=" * 60)

# Save models
print("\n📦 Saving models...")
joblib.dump(lgb_model, 'models/lgb_model.pkl')
print("  ✓ LightGBM model saved")

joblib.dump(xgb_model, 'models/xgb_model.pkl')
print("  ✓ XGBoost model saved")

joblib.dump(lr_model, 'models/lr_model.pkl')
print("  ✓ Logistic Regression model saved")

joblib.dump(nb_model, 'models/nb_model.pkl')
print("  ✓ Naive Bayes model saved")

# Save preprocessors
print("\n🔧 Saving preprocessors...")
joblib.dump(tfidf_word, 'models/tfidf_word.pkl')
print("  ✓ TF-IDF Word vectorizer saved")

joblib.dump(tfidf_char, 'models/tfidf_char.pkl')
print("  ✓ TF-IDF Char vectorizer saved")

joblib.dump(scaler, 'models/scaler.pkl')
print("  ✓ StandardScaler saved")

# Save feature names
feature_names = ['emoticon_1', 'emoticon_2', 'emoticon_3',
                 'upvote', 'downvote', 'if_1', 'if_2',
                 'comment_length', 'word_count']
joblib.dump(feature_names, 'models/feature_names.pkl')
print("  ✓ Feature names saved")

print("\n" + "=" * 60)
print("✅ ALL MODELS EXPORTED SUCCESSFULLY!")
print("=" * 60)

# Check file sizes
print("\n📊 Model file sizes:")
for filename in os.listdir('models'):
    filepath = os.path.join('models', filename)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  {filename}: {size_mb:.2f} MB")

print("\n🚀 Next steps:")
print("  1. Run: pip install -r requirements.txt")
print("  2. Run: python app.py")
print("  3. Test: python test_api.py")
print("\n" + "=" * 60)
```

## Alternative: If you get variable name errors

If your variable names are different in the notebook, adjust them accordingly:

```python
# Example if your variables have different names:
joblib.dump(your_lgb_model_name, 'models/lgb_model.pkl')
joblib.dump(your_xgb_model_name, 'models/xgb_model.pkl')
# ... etc
```

## Verify Export

After running the cell, verify the export:

```python
# Verify models were saved correctly
import os
print("Files in models/ directory:")
for f in os.listdir('models'):
    print(f"  ✓ {f}")
```
