import os
import joblib
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Constants for model paths
WESAD_MODEL_PATH = os.path.join("models", "ExtraTreeWESADModel01.pkl")
MMASH_MODEL_PATH = os.path.join("models", "MultiLayerPerceptron_MLP_MMASH_Model01.pkl")

# Expected feature order
WESAD_FEATURES = [
    "Mean_RR", "Mean_HR", "SDNN", "RMSSD", "pNN50",
    "SCR_Peaks_N", "SCR_Peaks_Amplitude_Mean", "EDA_Tonic_SD",
    "Resp_Rate_Mean", "Resp_Rate_Std", "Resp_Amplitude_Std",
    "Temp_Mean", "Temp_Std", "Temp_Min", "Temp_Max",
    "ACC_Magnitude_Mean", "ACC_Magnitude_Std", "ACC_Magnitude_Max"
]

MMASH_FEATURES = [
    "mean_hr", "sdnn", "rmssd"
]

class ModelService:
    def __init__(self):
        self.wesad_model = None
        self.mmash_model = None
        self._load_models()

    def _load_models(self):
        """Loads both models once when initialized."""
        try:
            self.wesad_model = joblib.load(WESAD_MODEL_PATH)
            logger.info("WESAD model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load WESAD model: {e}")
            raise

        try:
            self.mmash_model = joblib.load(MMASH_MODEL_PATH)
            logger.info("MMASH model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load MMASH model: {e}")
            raise

    def predict_wesad(self, features: dict) -> dict:
        """
        Runs WESAD model prediction.
        """
        # Validate features
        missing_features = [f for f in WESAD_FEATURES if f not in features]
        if missing_features:
            raise ValueError(f"Missing WESAD features: {missing_features}")

        # Preserve order
        ordered_features = {f: features[f] for f in WESAD_FEATURES}
        # Model expects 2D array-like input, best via DataFrame to maintain feature names internally
        df = pd.DataFrame([ordered_features])
        
        # We need to make sure we don't pass DataFrame to a model that strictly requires array
        # Scikit-learn 1.6.1 is generally fine with DataFrame. If issues arise, we can use df.values.
        # But we'll try DataFrame first to preserve feature names correctly.

        # Predict
        predicted_class = int(self.wesad_model.predict(df)[0])
        probabilities = self.wesad_model.predict_proba(df)[0]

        return {
            "predicted_class": predicted_class,
            "probability_class_0": float(probabilities[0]),
            "probability_class_1": float(probabilities[1])
        }

    def predict_mmash(self, features: dict) -> dict:
        """
        Runs MMASH model prediction.
        """
        # Validate features
        missing_features = [f for f in MMASH_FEATURES if f not in features]
        if missing_features:
            raise ValueError(f"Missing MMASH features: {missing_features}")

        # Preserve order
        ordered_features = {f: features[f] for f in MMASH_FEATURES}
        df = pd.DataFrame([ordered_features])

        # Predict
        predicted_class = int(self.mmash_model.predict(df)[0])
        probabilities = self.mmash_model.predict_proba(df)[0]

        return {
            "predicted_class": predicted_class,
            "probability_class_0": float(probabilities[0]),
            "probability_class_1": float(probabilities[1])
        }

# Singleton instance to be used across the application
model_service = ModelService()
