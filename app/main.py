from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model + imputer
model = pickle.load(open("water_quality_model.pkl", "rb"))
imputer = pickle.load(open("imputer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect input values from form
        features = [
            request.form.get("ph"),
            request.form.get("Hardness"),
            request.form.get("Solids"),
            request.form.get("Chloramines"),
            request.form.get("Sulfate"),
            request.form.get("Conductivity"),
            request.form.get("Organic_carbon"),
            request.form.get("Trihalomethanes"),
            request.form.get("Turbidity")
        ]
        
        # Convert to float, allow empty values as np.nan
        features = [float(x) if x.strip() != "" else np.nan for x in features]

        # Impute missing values
        features_imputed = imputer.transform([features])

        # Predict
        prediction = model.predict(features_imputed)[0]
        result = "✅ Potable (Safe to Drink)" if prediction == 1 else "🚱 Not Potable (Unsafe)"

        return render_template("result.html", result=result, values=features)

    except Exception as e:
        return f"Error: {e}"


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/table')
def table():
    return render_template('table.html')

if __name__ == "__main__":
    app.run('0.0.0.0' , debug=True , port=5005)

