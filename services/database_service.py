from datetime import datetime, timezone

from database.connection import db


users_collection = db["users"]
measurements_collection = db["measurements"]
predictions_collection = db["predictions"]
nsri_collection = db["nsri_results"]


def get_user_by_email(email: str):
    """Retrieve a user by their email address."""
    return users_collection.find_one({"email": email})


def create_user(name: str, email: str, password_hash: str):
    user = {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc),
    }

    result = users_collection.insert_one(user)

    return {
        "user_id": str(result.inserted_id),
        "name": name,
        "email": email,
        "created_at": user["created_at"],
    }


def save_measurement(user_id: str, data: dict):
    measurement = {
        "user_id": user_id,
        "recorded_at": datetime.now(timezone.utc),
        "data": data,
    }

    result = measurements_collection.insert_one(measurement)

    return str(result.inserted_id)


def save_prediction(user_id: str, measurement_id: str, data: dict):
    prediction = {
        "user_id": user_id,
        "measurement_id": measurement_id,
        "created_at": datetime.now(timezone.utc),
        "data": data,
    }

    result = predictions_collection.insert_one(prediction)

    return str(result.inserted_id)


def save_nsri_result(user_id: str, measurement_id: str, data: dict):
    result = {
        "user_id": user_id,
        "measurement_id": measurement_id,
        "created_at": datetime.now(timezone.utc),
        "data": data,
    }

    inserted = nsri_collection.insert_one(result)

    return str(inserted.inserted_id)
