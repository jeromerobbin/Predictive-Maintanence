import joblib

# Load the saved files
model = joblib.load("models/predictive_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoder = joblib.load("models/encoder.pkl")

# Check if they are loaded properly 
print(model)      # Should print RandomForestClassifier details
print(scaler)     # Should print StandardScaler details
print(encoder)    # Should print LabelEncoder details
