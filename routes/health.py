from fastapi import APIRouter
from services.model_service import model_service

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "wesad_model_loaded": model_service.wesad_model is not None,
        "mmash_model_loaded": model_service.mmash_model is not None
    }
