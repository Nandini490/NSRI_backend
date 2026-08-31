import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def run_tests():
    print("--- Starting NSRI API Tests ---\n")

    # 1. Valid SAI and PRI
    print("1. Testing valid SAI and PRI calculation...")
    payload = {
        "wesad_stress_probability": 0.7,
        "mmash_stress_probability": 0.5,
        "hrv_normalized": 0.8,
        "resting_hr_normalized": 0.3
    }
    response = client.post("/api/v1/nsri/calculate", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200
    assert response.json()["sai"] == 60.0
    assert response.json()["pri"] == 76.0

    # 2. Valid SAI only
    print("2. Testing valid SAI only...")
    payload = {
        "wesad_stress_probability": 0.85
    }
    response = client.post("/api/v1/nsri/calculate", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200
    assert response.json()["sai"] == 85.0
    assert response.json()["pri"] is None

    # 3. Valid PRI only
    print("3. Testing valid PRI only...")
    payload = {
        "hrv_normalized": 0.5,
        "resting_hr_normalized": 0.5
    }
    response = client.post("/api/v1/nsri/calculate", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200
    assert response.json()["sai"] is None
    assert response.json()["pri"] == 50.0

    # 4. Invalid - Empty payload
    print("4. Testing empty payload...")
    payload = {}
    response = client.post("/api/v1/nsri/calculate", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 422

    # 5. Invalid - Missing one PRI input
    print("5. Testing missing one PRI input...")
    payload = {
        "hrv_normalized": 0.8
    }
    response = client.post("/api/v1/nsri/calculate", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 422
    assert "Both hrv_normalized and resting_hr_normalized are required" in response.json()["detail"]

    # 6. Invalid - Data type error (e.g. string instead of float)
    print("6. Testing invalid data type...")
    payload = {
        "wesad_stress_probability": "invalid_string"
    }
    response = client.post("/api/v1/nsri/calculate", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 422

    print("--- All NSRI API Tests Completed Successfully ---")

if __name__ == "__main__":
    run_tests()
