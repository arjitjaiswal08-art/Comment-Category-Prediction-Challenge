"""
Test script for the Comment Category Prediction API
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_single_prediction():
    """Test single prediction"""
    print("Testing /predict endpoint...")
    
    # Sample data
    data = {
        "comment": "This is a great article! I really enjoyed reading it.",
        "emoticon_1": 1,
        "emoticon_2": 0,
        "emoticon_3": 0,
        "upvote": 5,
        "downvote": 0,
        "if_1": 0,
        "if_2": 10
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_batch_prediction():
    """Test batch prediction"""
    print("Testing /batch_predict endpoint...")
    
    # Sample batch data
    data = {
        "comments": [
            {
                "comment": "This is amazing!",
                "emoticon_1": 1,
                "emoticon_2": 0,
                "emoticon_3": 0,
                "upvote": 10,
                "downvote": 0,
                "if_1": 0,
                "if_2": 5
            },
            {
                "comment": "This is terrible and disappointing.",
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
    
    response = requests.post(
        f"{BASE_URL}/batch_predict",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == '__main__':
    print("=" * 60)
    print("API TESTING SCRIPT")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_single_prediction()
        test_batch_prediction()
        
        print("=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API")
        print("Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
