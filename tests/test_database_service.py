import sys
import os
import datetime
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.database_service import create_user

@patch('services.database_service.users_collection')
def test_create_user(mock_users_collection):
    """Test user creation properly stores the password hash."""
    print("\n--- Test: Create User with password hash ---")
    
    # Mock the insert_one response
    mock_result = MagicMock()
    mock_result.inserted_id = "test_object_id_12345"
    mock_users_collection.insert_one.return_value = mock_result
    
    name = "Test User"
    email = "test@example.com"
    password_hash = "$2b$12$testHashedPasswordString1234567890"
    
    # Call create_user
    result = create_user(name, email, password_hash)
    
    # Assert insert_one was called correctly
    mock_users_collection.insert_one.assert_called_once()
    call_args = mock_users_collection.insert_one.call_args[0][0]
    
    assert call_args["name"] == name
    assert call_args["email"] == email
    assert call_args["password_hash"] == password_hash
    assert "created_at" in call_args
    
    # Ensure plaintext password is NOT in the arguments
    assert "password" not in call_args
    
    # Assert return object structure
    assert result["user_id"] == "test_object_id_12345"
    assert result["name"] == name
    assert result["email"] == email
    assert "password_hash" not in result  # Should not be returned in user profile response
    
    print("  PASSED")

if __name__ == "__main__":
    print("=" * 50)
    print("  Database Service Tests")
    print("=" * 50)
    
    test_create_user()
    
    print("\n" + "=" * 50)
    print("  All Database Service tests PASSED!")
    print("=" * 50)
