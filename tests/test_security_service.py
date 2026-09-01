import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.security_service import security_service
from datetime import timedelta

def test_password_hashing_and_verification():
    print("\n--- Test: Password Hashing & Verification ---")
    password = "SuperSecretPassword123!"
    
    # Hash password
    hashed = security_service.get_password_hash(password)
    print(f"  Generated hash: {hashed[:15]}...")
    
    assert hashed != password
    assert len(hashed) > 10
    
    # Verify correct password
    assert security_service.verify_password(password, hashed) is True
    print("  Password correctly verified.")
    
    # Verify incorrect password
    assert security_service.verify_password("wrongpassword", hashed) is False
    print("  Incorrect password correctly rejected.")
    print("  PASSED")


def test_token_creation_and_decoding():
    print("\n--- Test: JWT Token Creation & Decoding ---")
    data = {"sub": "user_id_12345", "role": "admin"}
    
    # Create token
    token = security_service.create_access_token(data=data)
    print(f"  Generated token: {token[:20]}...")
    assert isinstance(token, str)
    
    # Decode token
    decoded = security_service.decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user_id_12345"
    assert decoded["role"] == "admin"
    assert "exp" in decoded
    print("  Token successfully decoded and payload verified.")
    print("  PASSED")


def test_token_expiration():
    print("\n--- Test: JWT Token Expiration Validation ---")
    data = {"sub": "user_id_67890"}
    
    # Create a token that expires very quickly (negative delta to expire immediately)
    token = security_service.create_access_token(data=data, expires_delta=timedelta(seconds=-1))
    
    # Attempt to decode the expired token
    decoded = security_service.decode_access_token(token)
    
    # Validation should fail and return None
    assert decoded is None
    print("  Expired token correctly rejected.")
    print("  PASSED")


def test_invalid_token_decoding():
    print("\n--- Test: Invalid JWT Token Decoding ---")
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalidpayload.invalidsignature"
    
    decoded = security_service.decode_access_token(invalid_token)
    
    assert decoded is None
    print("  Invalid token correctly rejected.")
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 50)
    print("  Security Service Tests")
    print("=" * 50)
    
    test_password_hashing_and_verification()
    test_token_creation_and_decoding()
    test_token_expiration()
    test_invalid_token_decoding()
    
    print("\n" + "=" * 50)
    print("  All Security Service tests PASSED!")
    print("=" * 50)
