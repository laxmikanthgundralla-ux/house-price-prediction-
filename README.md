# HomeValue — House Price Prediction

A Flask web app that estimates a house price from location, built-up area, bedrooms, bathrooms, and property age. The public-facing website is intentionally focused on property price prediction; it does not show technology lists or model-accuracy analysis.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Train the model:
   ```bash
   python train_model.py
   ```
6. Start the website:
   ```bash
   python app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.

## Dataset notice

`data/house_prices.csv` is a **synthetic demonstration dataset** generated for this starter project. It is not a verified record of actual market transactions, so the model's predictions must not be treated as real property valuations. Before using the app for real estimates, replace this file with a reliable, appropriately licensed housing dataset with the same column names, then retrain the model.

Required columns: `location`, `area_sqft`, `bedrooms`, `bathrooms`, `age_years`, `price_inr`.

## GitHub

Create a new empty repository on GitHub, then run these commands from this folder:

```bash
git init
git add .
git commit -m "Build house price prediction app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example remote with your own repository URL. Do not commit `.venv/` or secret credentials.
