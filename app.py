from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load model and preprocessing tools
model = joblib.load("models/predictive_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoder = joblib.load("models/encoder.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from frontend
        data = request.json  

        # Extract input values
        motor_type = data['Type']
        air_temp = float(data['Air_temperature'])
        process_temp = float(data['Process_temperature'])
        rotational_speed = float(data['Rotational_speed'])
        torque = float(data['Torque'])
        tool_wear = float(data['Tool_wear'])

        # Encode motor type
        if motor_type not in encoder.classes_:
            return jsonify({"error": f"Invalid Type! Expected one of {encoder.classes_.tolist()}"}), 400
        motor_type_encoded = encoder.transform([motor_type])[0]

        # Prepare input as DataFrame
        input_data = pd.DataFrame([[motor_type_encoded, air_temp, process_temp, rotational_speed, torque, tool_wear]],
                                  columns=["Type", "Air temperature [K]", "Process temperature [K]", 
                                           "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"])

        # Scale input
        scaled_input = scaler.transform(input_data)

        # Make prediction
        result = model.predict(scaled_input)

        # Determine message
        message = ("⚠️ High chances of machine failure. Immediate attention required."
                   if result[0] == 1 else 
                   "✅ No failure detected. Machine is performing well.")

        return jsonify({"prediction": int(result[0]), "message": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
