import pytest
import numpy as np
from src.data_loader import load_data
import joblib
import os

def test_data_shape():
    """Test if data loads correctly"""
    df = load_data()
    assert df.shape[0] > 0
    assert df.shape[1] >= 14 # 14 features + target [cite: 10]

def test_model_prediction_shape():
    """Test if the saved model produces valid predictions"""
    if not os.path.exists("models/best_model.pkl"):
        pytest.skip("Model file not found. Run training first.")
    
    model = joblib.load("models/best_model.pkl")
    # Create dummy input with 13 features (dataset specific)
    sample_input = np.random.rand(1, 13)
    prediction = model.predict(sample_input)
    assert len(prediction) == 1
    assert prediction[0] in [0, 1]