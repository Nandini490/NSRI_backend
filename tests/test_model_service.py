import sys
import os

# Add the root directory to sys.path so we can import services
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.model_service import model_service
import json

def test_wesad():
    print("\n--- Testing WESAD Model ---")
    
    # Realistic values for WESAD features
    wesad_features = {
        "Mean_RR": 0.85,
        "Mean_HR": 75.0,
        "SDNN": 0.05,
        "RMSSD": 0.03,
        "pNN50": 0.15,
        "SCR_Peaks_N": 5.0,
        "SCR_Peaks_Amplitude_Mean": 0.1,
        "EDA_Tonic_SD": 0.02,
        "Resp_Rate_Mean": 16.0,
        "Resp_Rate_Std": 2.5,
        "Resp_Amplitude_Std": 1.2,
        "Temp_Mean": 34.5,
        "Temp_Std": 0.1,
        "Temp_Min": 34.0,
        "Temp_Max": 35.0,
        "ACC_Magnitude_Mean": 1.0,
        "ACC_Magnitude_Std": 0.05,
        "ACC_Magnitude_Max": 1.5
    }

    try:
        result = model_service.predict_wesad(wesad_features)
        print("WESAD Prediction successful!")
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"WESAD Prediction failed: {e}")

def test_mmash():
    print("\n--- Testing MMASH Model ---")
    
    # Realistic values for MMASH features
    mmash_features = {
        "mean_hr": 70.0,
        "sdnn": 50.0,
        "rmssd": 35.0
    }

    try:
        result = model_service.predict_mmash(mmash_features)
        print("MMASH Prediction successful!")
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"MMASH Prediction failed: {e}")

if __name__ == "__main__":
    print("Initializing tests for ModelService...")
    test_wesad()
    test_mmash()
    print("\nTests completed.")
