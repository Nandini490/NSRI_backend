import sys
import os
from datetime import timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from dependencies.auth import get_current_user_token
from services.security_service import security_service

# Setup a dummy app to test the dependency
test_app = FastAPI()

@test_app.get("/protected-route")
def protected_route(user_id: str = Depends(get_current_user_token)):
    return {"message": "You are authorized", "user_id": user_id}

client = TestClient(test_app)

def test_valid_token():
    print("\n--- Test: Valid Token ---")
    valid_token = security_service.create_access_token(data={"sub": "user_789"})
    
    response = client.get("/protected-route", headers={"Authorization": f"Bearer {valid_token}"})
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200
    assert response.json() == {"message": "You are authorized", "user_id": "user_789"}
    print("  PASSED (Authorized)")

def test_missing_token():
    print("\n--- Test: Missing Token ---")
    
    response = client.get("/protected-route")
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    print("  PASSED (Blocked)")

def test_invalid_token():
    print("\n--- Test: Invalid Token ---")
    
    response = client.get("/protected-route", headers={"Authorization": "Bearer invalid.token.string"})
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    print("  PASSED (Blocked)")

def test_expired_token():
    print("\n--- Test: Expired Token ---")
    
    # Create an explicitly expired token
    expired_token = security_service.create_access_token(
        data={"sub": "user_789"}, 
        expires_delta=timedelta(seconds=-1)
    )
    
    response = client.get("/protected-route", headers={"Authorization": f"Bearer {expired_token}"})
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    print("  PASSED (Blocked)")

if __name__ == "__main__":
    print("=" * 50)
    print("  API Auth Dependency Tests")
    print("=" * 50)
    
    test_valid_token()
    test_missing_token()
    test_invalid_token()
    test_expired_token()
    
    print("\n" + "=" * 50)
    print("  All Auth Dependency tests PASSED!")
    print("=" * 50)
