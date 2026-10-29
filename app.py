from flask import Flask, render_template, request
from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "house_price_model.joblib"
APP = Flask(__name__)

model = None
model_error = None
try:
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    else:
        model_error = "The prediction model has not been trained yet. Run train_model.py first."
except Exception as exc:
    model_error = f"Could not load the prediction model: {exc}"

LOCATIONS = ["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Delhi", "Pune", "Kolkata", "Other"]

@APP.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    price_low = None
    price_high = None
    error = None
    values = {
        "location": "Hyderabad",
        "area": "1500",
        "bedrooms": "3",
        "bathrooms": "2",
        "age": "5",
    }

    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        try:
            location = values["location"]
            area = float(values["area"])
            bedrooms = int(values["bedrooms"])
            bathrooms = int(values["bathrooms"])
            age = float(values["age"])

            if location not in LOCATIONS:
                raise ValueError("Please select a valid location.")
            if area < 200 or area > 20000:
                raise ValueError("Area must be between 200 and 20,000 square feet.")
            if not 1 <= bedrooms <= 15:
                raise ValueError("Bedrooms must be between 1 and 15.")
            if not 1 <= bathrooms <= 15:
                raise ValueError("Bathrooms must be between 1 and 15.")
            if not 0 <= age <= 150:
                raise ValueError("Property age must be between 0 and 150 years.")
            if model is None:
                raise RuntimeError(model_error or "Prediction model is unavailable.")

            features = pd.DataFrame([{
                "location": location,
                "area_sqft": area,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "age_years": age,
            }])
            # Model predicts price in Indian rupees.
            prediction = max(0, float(model.predict(features)[0]))
            # This is a simple illustrative range, not a calibrated confidence interval.
            price_low = prediction * 0.90
            price_high = prediction * 1.10
        except (ValueError, TypeError) as exc:
            error = str(exc) or "Please enter valid property details."
        except RuntimeError as exc:
            error = str(exc)
        except Exception:
            error = "We couldn't calculate a price for these details. Please try again."

    return render_template(
        "index.html",
        prediction=prediction,
        price_low=price_low,
        price_high=price_high,
        error=error,
        values=values,
        locations=LOCATIONS,
    )

if __name__ == "__main__":
    APP.run(host="127.0.0.1", port=5000, debug=True)
