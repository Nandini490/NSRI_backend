import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def run_tests():
    print("--- Starting API Tests ---\n")

    # 1. Health check
    print("1. Testing Health Endpoint...")
    response = client.get("/api/v1/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200

    # 2. WESAD valid prediction
    print("2. Testing WESAD valid prediction...")
    wesad_payload = {
        "Mean_RR": 0.85,
        "Mean_HR": 75.0,
        "SDNN": 0.07,
        "RMSSD": 0.05,
        "pNN50": 25.0,
        "SCR_Peaks_N": 20.0,
        "SCR_Peaks_Amplitude_Mean": 0.02,
        "EDA_Tonic_SD": 0.15,
        "Resp_Rate_Mean": 18.0,
        "Resp_Rate_Std": 2.0,
        "Resp_Amplitude_Std": 1.5,
        "Temp_Mean": 32.0,
        "Temp_Std": 0.05,
        "Temp_Min": 31.9,
        "Temp_Max": 32.1,
        "ACC_Magnitude_Mean": 0.95,
        "ACC_Magnitude_Std": 0.01,
        "ACC_Magnitude_Max": 0.98
    }
    response = client.post("/api/v1/predict/wesad", json=wesad_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200
    assert response.json()["model"] == "WESAD"

    # 3. MMASH valid prediction
    print("3. Testing MMASH valid prediction...")
    mmash_payload = {
        "mean_hr": 70.0,
        "sdnn": 50.0,
        "rmssd": 35.0
    }
    response = client.post("/api/v1/predict/mmash", json=mmash_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200
    assert response.json()["model"] == "MMASH"

    # 4. WESAD invalid payload (missing feature)
    print("4. Testing WESAD invalid prediction (missing feature)...")
    invalid_wesad_payload = wesad_payload.copy()
    del invalid_wesad_payload["Mean_HR"]
    response = client.post("/api/v1/predict/wesad", json=invalid_wesad_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 422

    # 5. MMASH invalid payload (non-numeric feature)
    print("5. Testing MMASH invalid prediction (non-numeric feature)...")
    invalid_mmash_payload = mmash_payload.copy()
    invalid_mmash_payload["sdnn"] = "invalid_string"
    response = client.post("/api/v1/predict/mmash", json=invalid_mmash_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 422

    print("--- All Tests Completed Successfully ---")

if __name__ == "__main__":
    run_tests()
