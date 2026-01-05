import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo  # Suggested method for UCI datasets

def load_data():
    # Fetch dataset using UCI library or direct URL
    # Heart Disease UCI ID is 45
    print("Downloading dataset...")
    heart_disease = fetch_ucirepo(id=45) 
    
    X = heart_disease.data.features
    y = heart_disease.data.targets
    
    # Combine for EDA/cleaning
    df = pd.concat([X, y], axis=1)
    
    # Handling missing values (ca and thal have missing values in this dataset)
    df = df.dropna()
    
    print(f"Data loaded successfully. Shape: {df.shape}")
    return df

def save_data(df, filepath="data/heart.csv"):
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    df = load_data()
    save_data(df)