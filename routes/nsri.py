from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.nsri_service import nsri_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class NSRIRequest(BaseModel):
    wesad_stress_probability: Optional[float] = None
    mmash_stress_probability: Optional[float] = None
    hrv_normalized: Optional[float] = None
    resting_hr_normalized: Optional[float] = None

@router.post("/calculate")
def calculate_nsri(request: NSRIRequest):
    # Validate that at least one required input is provided
    if (request.wesad_stress_probability is None and 
        request.mmash_stress_probability is None and 
        request.hrv_normalized is None and 
        request.resting_hr_normalized is None):
        raise HTTPException(
            status_code=422, 
            detail="At least one input must be provided to calculate NSRI metrics."
        )

    # Validate that PRI inputs are both provided if one is provided
    if (request.hrv_normalized is not None and request.resting_hr_normalized is None) or \
       (request.hrv_normalized is None and request.resting_hr_normalized is not None):
        raise HTTPException(
            status_code=422, 
            detail="Both hrv_normalized and resting_hr_normalized are required to calculate PRI."
        )

    try:
        sai = nsri_service.calculate_sai(
            wesad_stress_probability=request.wesad_stress_probability,
            mmash_stress_probability=request.mmash_stress_probability
        )
        
        pri = nsri_service.calculate_pri(
            hrv_normalized=request.hrv_normalized,
            resting_hr_normalized=request.resting_hr_normalized
        )

        return {
            "sai": sai,
            "pri": pri
        }
    except Exception as e:
        logger.error(f"NSRI Calculation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during NSRI calculation")
