"""
Export trained models from Jupyter notebook
Run this script after training your models in the notebook
"""

import joblib
import os
import sys

def export_models():
    """
    Export all trained models and preprocessors to the models/ directory
    
    This script should be run from within your Jupyter notebook after training,
    or you can modify it to load from your notebook's variables.
    """
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    print("=" * 60)
    print("MODEL EXPORT SCRIPT")
    print("=" * 60)
    print("\nThis script will help you export your trained models.")
    print("\nIMPORTANT: You need to run this from your Jupyter notebook")
    print("after training all models, or modify this script to load")
    print("your trained models from saved files.\n")
    
    print("Expected models to export:")
    print("  1. lgb_model (LightGBM)")
    print("  2. xgb_model (XGBoost)")
    print("  3. lr_model (Logistic Regression)")
    print("  4. nb_model (Naive Bayes)")
    print("  5. tfidf_word (TF-IDF Word Vectorizer)")
    print("  6. tfidf_char (TF-IDF Char Vectorizer)")
    print("  7. scaler (StandardScaler)")
    print("  8. feature_names (list)")
    
    print("\n" + "=" * 60)
    print("INSTRUCTIONS:")
    print("=" * 60)
    print("\n1. In your Jupyter notebook, after training all models, add:")
    print("\n   import joblib")
    print("   import os")
    print("   ")
    print("   os.makedirs('models', exist_ok=True)")
    print("   ")
    print("   # Save models")
    print("   joblib.dump(lgb_model, 'models/lgb_model.pkl')")
    print("   joblib.dump(xgb_model, 'models/xgb_model.pkl')")
    print("   joblib.dump(lr_model, 'models/lr_model.pkl')")
    print("   joblib.dump(nb_model, 'models/nb_model.pkl')")
    print("   ")
    print("   # Save preprocessors")
    print("   joblib.dump(tfidf_word, 'models/tfidf_word.pkl')")
    print("   joblib.dump(tfidf_char, 'models/tfidf_char.pkl')")
    print("   joblib.dump(scaler, 'models/scaler.pkl')")
    print("   ")
    print("   # Save feature names")
    print("   feature_names = ['emoticon_1', 'emoticon_2', 'emoticon_3',")
    print("                    'upvote', 'downvote', 'if_1', 'if_2',")
    print("                    'comment_length', 'word_count']")
    print("   joblib.dump(feature_names, 'models/feature_names.pkl')")
    print("   ")
    print("   print('✓ All models exported successfully!')")
    
    print("\n2. Run the cells in your notebook")
    print("\n3. Then start the Flask API with: python app.py")
    
    print("\n" + "=" * 60)
    
    # Check if models directory exists and has files
    if os.path.exists('models'):
        files = os.listdir('models')
        if files:
            print("\nFound existing files in models/ directory:")
            for f in files:
                size = os.path.getsize(os.path.join('models', f)) / (1024 * 1024)
                print(f"  ✓ {f} ({size:.2f} MB)")
            print("\n✓ Models appear to be exported!")
            return True
        else:
            print("\n✗ models/ directory is empty")
            return False
    else:
        print("\n✗ models/ directory does not exist")
        return False

if __name__ == '__main__':
    export_models()
