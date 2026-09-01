import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
import pytest

client = TestClient(app)

def test_successful_signup():
    print("\n--- Test: Successful Signup ---")
    
    mock_get_user = patch('routes.auth.get_user_by_email').start()
    mock_create_user = patch('routes.auth.create_user').start()
    
    # Setup mocks
    mock_get_user.return_value = None  # No existing user
    mock_create_user.return_value = {
        "user_id": "new_user_123",
        "name": "Nandini",
        "email": "test@example.com",
        "created_at": "2026-09-01T12:00:00Z"
    }
    
    payload = {
        "name": "Nandini",
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }
    
    response = client.post("/api/v1/auth/signup", json=payload)
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 201
    
    data = response.json()
    assert data["message"] == "User created successfully"
    assert data["user_id"] == "new_user_123"
    assert data["name"] == "Nandini"
    assert data["email"] == "test@example.com"
    
    # VERIFY plaintext password is NOT passed to create_user
    mock_create_user.assert_called_once()
    called_kwargs = mock_create_user.call_args.kwargs
    assert called_kwargs["name"] == "Nandini"
    assert called_kwargs["email"] == "test@example.com"
    assert "password" not in called_kwargs
    assert "password_hash" in called_kwargs
    # Ensure it's a hash and not the plaintext
    assert called_kwargs["password_hash"] != "SecurePassword123!"
    assert len(called_kwargs["password_hash"]) > 20
    
    print("  PASSED (Password properly hashed, plaintext not stored)")
    
    patch.stopall()

def test_duplicate_email_signup():
    print("\n--- Test: Duplicate Email Signup ---")
    
    mock_get_user = patch('routes.auth.get_user_by_email').start()
    mock_create_user = patch('routes.auth.create_user').start()
    
    # Setup mock to simulate existing user
    mock_get_user.return_value = {"email": "duplicate@example.com", "name": "Existing User"}
    
    payload = {
        "name": "New User",
        "email": "duplicate@example.com",
        "password": "Password123"
    }
    
    response = client.post("/api/v1/auth/signup", json=payload)
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]
    
    # Verify create_user was NEVER called
    mock_create_user.assert_not_called()
    
    print("  PASSED (Duplicate email blocked, 409 returned)")
    
    patch.stopall()

def test_invalid_signup_payload():
    print("\n--- Test: Invalid Signup Payload ---")
    
    # Missing email
    payload = {
        "name": "No Email User",
        "password": "Password123"
    }
    
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 422
    
    # Invalid email format
    payload = {
        "name": "Bad Email User",
        "email": "not-an-email",
        "password": "Password123"
    }
    
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 422
    
    print("  PASSED (Basic validation working)")

def test_successful_login():
    print("\n--- Test: Successful Login ---")
    mock_get_user = patch('routes.auth.get_user_by_email').start()
    mock_verify = patch('routes.auth.security_service.verify_password').start()
    mock_create_token = patch('routes.auth.security_service.create_access_token').start()
    
    mock_get_user.return_value = {
        "_id": "user_123",
        "email": "test@example.com",
        "password_hash": "hashed_pw"
    }
    mock_verify.return_value = True
    mock_create_token.return_value = "mocked_jwt_token_123"
    
    payload = {
        "email": "test@example.com",
        "password": "CorrectPassword123!"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "mocked_jwt_token_123"
    assert data["token_type"] == "bearer"
    assert "password" not in data
    assert "password_hash" not in data
    
    print("  PASSED (Token returned, no sensitive data)")
    patch.stopall()

def test_unknown_email_login():
    print("\n--- Test: Unknown Email Login ---")
    mock_get_user = patch('routes.auth.get_user_by_email').start()
    
    mock_get_user.return_value = None
    
    payload = {
        "email": "unknown@example.com",
        "password": "Password123"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
    
    print("  PASSED (Unknown email blocked)")
    patch.stopall()

def test_incorrect_password_login():
    print("\n--- Test: Incorrect Password Login ---")
    mock_get_user = patch('routes.auth.get_user_by_email').start()
    mock_verify = patch('routes.auth.security_service.verify_password').start()
    
    mock_get_user.return_value = {
        "_id": "user_123",
        "email": "test@example.com",
        "password_hash": "hashed_pw"
    }
    mock_verify.return_value = False
    
    payload = {
        "email": "test@example.com",
        "password": "WrongPassword!"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
    
    print("  PASSED (Incorrect password blocked)")
    patch.stopall()


if __name__ == "__main__":
    print("=" * 50)
    print("  API Auth Tests")
    print("=" * 50)
    
    test_successful_signup()
    test_duplicate_email_signup()
    test_invalid_signup_payload()
    
    test_successful_login()
    test_unknown_email_login()
    test_incorrect_password_login()
    
    print("\n" + "=" * 50)
    print("  All API Auth tests PASSED!")
    print("=" * 50)
