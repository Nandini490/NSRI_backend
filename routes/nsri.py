from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.nsri_service import nsri_service
from services.database_service import save_nsri_result
from services.external_factor_service import external_factor_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class NSRIRequest(BaseModel):
    wesad_stress_probability: Optional[float] = None
    mmash_stress_probability: Optional[float] = None
    hrv_normalized: Optional[float] = None
    resting_hr_normalized: Optional[float] = None
    external_stress_score: Optional[float] = None
    # External factor service options
    fetch_external_stress: Optional[bool] = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    user_id: Optional[str] = None
    measurement_id: Optional[str] = None

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

    # Validate that PRI/RDT inputs are both provided if one is provided
    if (request.hrv_normalized is not None and request.resting_hr_normalized is None) or \
       (request.hrv_normalized is None and request.resting_hr_normalized is not None):
        raise HTTPException(
            status_code=422, 
            detail="Both hrv_normalized and resting_hr_normalized are required to calculate PRI and RDT."
        )

    try:
        # Fetch external stress score if requested
        external_stress_score = request.external_stress_score
        if request.fetch_external_stress and external_stress_score is None:
            external_stress_score = external_factor_service.calculate_external_stress_score(
                latitude=request.latitude,
                longitude=request.longitude
            )
            if external_stress_score is not None:
                logger.info(f"Fetched external stress score: {external_stress_score}")
            else:
                logger.info("External stress score not available; using None")

        sai = nsri_service.calculate_sai(
            wesad_stress_probability=request.wesad_stress_probability,
            mmash_stress_probability=request.mmash_stress_probability
        )
        
        pri = nsri_service.calculate_pri(
            hrv_normalized=request.hrv_normalized,
            resting_hr_normalized=request.resting_hr_normalized
        )

        rdt = nsri_service.calculate_rdt(
            hrv_normalized=request.hrv_normalized,
            resting_hr_normalized=request.resting_hr_normalized,
            external_stress_score=external_stress_score
        )

        nsri = nsri_service.calculate_nsri(
            sai=sai,
            pri=pri,
            rdt=rdt
        )

        result_data = {
            "sai": sai,
            "pri": pri,
            "external_stress_score": external_stress_score,
            "rdt": rdt,
            "nsri": nsri
        }

        # Save NSRI result to database if both user_id and measurement_id are provided
        if request.user_id and request.measurement_id:
            try:
                save_nsri_result(
                    user_id=request.user_id,
                    measurement_id=request.measurement_id,
                    data=result_data
                )
            except Exception as e:
                logger.error(f"Failed to save NSRI result to database: {e}")
                # Continue to return the result even if saving fails

        return result_data
    except Exception as e:
        logger.error(f"NSRI Calculation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during NSRI calculation")
