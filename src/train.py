import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
import joblib

def train_model():
    # Load Data
    df = pd.read_csv("data/heart.csv")
    X = df.drop("num", axis=1) # Target variable
    y = (df["num"] > 0).astype(int) # Binary classification: 0=No disease, 1=Disease

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Set up Experiment
    mlflow.set_experiment("Heart_Disease_Prediction")

    # Define models to train
    models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000),
        "Random_Forest": RandomForestClassifier(n_estimators=100)
    }

    best_model = None
    best_acc = 0

    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            # Create Pipeline [cite: 30]
            pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('classifier', model)
            ])

            # Train
            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)
            probs = pipeline.predict_proba(X_test)[:, 1]

            # Metrics [cite: 20]
            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds)
            rec = recall_score(y_test, preds)
            roc = roc_auc_score(y_test, probs)

            # Log to MLflow [cite: 23]
            mlflow.log_param("model_type", name)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("roc_auc", roc)
            
            # Log Model
            mlflow.sklearn.log_model(pipeline, "model")
            
            print(f"{name} - Accuracy: {acc:.4f}")

            # Save best model locally for containerization
            if acc > best_acc:
                best_acc = acc
                best_model = pipeline
                joblib.dump(best_model, "models/best_model.pkl")

if __name__ == "__main__":
    train_model()