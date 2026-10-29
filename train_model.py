"""Train a house-price model from the included sample dataset.

The included data is synthetic and is only for demonstrating the full application
workflow. Replace it with a suitable real housing dataset before relying on estimates.
"""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "house_prices.csv"
MODEL_PATH = BASE_DIR / "house_price_model.joblib"

def main():
    df = pd.read_csv(DATA_PATH)
    required = ["location", "area_sqft", "bedrooms", "bathrooms", "age_years", "price_inr"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

    df = df[required].dropna()
    X = df[["location", "area_sqft", "bedrooms", "bathrooms", "age_years"]]
    y = df["price_inr"]

    categorical = ["location"]
    numeric = ["area_sqft", "bedrooms", "bathrooms", "age_years"]
    preprocessor = ColumnTransformer([
        ("location", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", "passthrough", numeric),
    ])
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(n_estimators=250, random_state=42, min_samples_leaf=2)),
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model trained on {len(df)} rows and saved to: {MODEL_PATH}")
    print("Important: this starter dataset is synthetic; predictions are for demonstration only.")

if __name__ == "__main__":
    main()
