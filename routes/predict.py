from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.model_service import model_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class WESADRequest(BaseModel):
    Mean_RR: float
    Mean_HR: float
    SDNN: float
    RMSSD: float
    pNN50: float
    SCR_Peaks_N: float
    SCR_Peaks_Amplitude_Mean: float
    EDA_Tonic_SD: float
    Resp_Rate_Mean: float
    Resp_Rate_Std: float
    Resp_Amplitude_Std: float
    Temp_Mean: float
    Temp_Std: float
    Temp_Min: float
    Temp_Max: float
    ACC_Magnitude_Mean: float
    ACC_Magnitude_Std: float
    ACC_Magnitude_Max: float

class MMASHRequest(BaseModel):
    mean_hr: float
    sdnn: float
    rmssd: float

@router.post("/wesad")
def predict_wesad(request: WESADRequest):
    if model_service.wesad_model is None:
        raise HTTPException(status_code=503, detail="WESAD model not loaded")
    
    try:
        features = request.model_dump()
        result = model_service.predict_wesad(features)
        return {
            "model": "WESAD",
            "predicted_class": result["predicted_class"],
            "probability_class_0": result["probability_class_0"],
            "probability_class_1": result["probability_class_1"]
        }
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"WESAD Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during WESAD prediction")

@router.post("/mmash")
def predict_mmash(request: MMASHRequest):
    if model_service.mmash_model is None:
        raise HTTPException(status_code=503, detail="MMASH model not loaded")
    
    try:
        features = request.model_dump()
        result = model_service.predict_mmash(features)
        return {
            "model": "MMASH",
            "predicted_class": result["predicted_class"],
            "probability_class_0": result["probability_class_0"],
            "probability_class_1": result["probability_class_1"]
        }
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"MMASH Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during MMASH prediction")
