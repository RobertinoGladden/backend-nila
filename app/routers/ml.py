"""Machine Learning router for predictions and recommendations"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.ml_service import (
    estimate_harvest_date, get_harvest_predictions,
    recommend_feeding, get_feeding_recommendations,
    get_active_ml_models, get_model_performance
)
from app.schemas import (
    HarvestPredictionResponse, FeedingRecommendationResponse
)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


def get_user_from_token(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Dependency to get user from token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(db, token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user


# ── HARVEST ESTIMATION ─────────────────────────────────────────

@router.post("/harvest-estimate/{farming_cycle_id}", response_model=HarvestPredictionResponse)
def predict_harvest(
    farming_cycle_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Generate harvest date estimation for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        prediction = estimate_harvest_date(db, farming_cycle_id)
        return prediction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/harvest-estimate/{farming_cycle_id}", response_model=List[HarvestPredictionResponse])
def get_harvest_estimates(
    farming_cycle_id: int,
    limit: int = 10,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get all harvest predictions for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    predictions = get_harvest_predictions(db, farming_cycle_id)
    return predictions[:limit]


# ── FEEDING RECOMMENDATIONS ────────────────────────────────────

@router.post("/feeding-recommend/{farming_cycle_id}", response_model=FeedingRecommendationResponse)
def recommend_feeding_endpoint(
    farming_cycle_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Generate feeding recommendation for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        recommendation = recommend_feeding(db, farming_cycle_id)
        return recommendation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@router.get("/feeding-recommend/{farming_cycle_id}", response_model=List[FeedingRecommendationResponse])
def get_feeding_recommendations_endpoint(
    farming_cycle_id: int,
    limit: int = 10,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get recent feeding recommendations for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    recommendations = get_feeding_recommendations(db, farming_cycle_id, limit)
    return recommendations


# ── ML MODELS ──────────────────────────────────────────────────

@router.get("/models", response_model=dict)
def list_active_models(
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get all active ML models
    """
    models = get_active_ml_models(db)
    return {
        "harvest_estimation_model": {
            "id": models["harvest_estimation"].id if models["harvest_estimation"] else None,
            "version": models["harvest_estimation"].model_version if models["harvest_estimation"] else None,
            "accuracy": models["harvest_estimation"].accuracy if models["harvest_estimation"] else None
        } if models["harvest_estimation"] else None,
        "feeding_decision_model": {
            "id": models["feeding_decision"].id if models["feeding_decision"] else None,
            "version": models["feeding_decision"].model_version if models["feeding_decision"] else None,
            "accuracy": models["feeding_decision"].accuracy if models["feeding_decision"] else None
        } if models["feeding_decision"] else None
    }


@router.get("/models/{model_id}/performance", response_model=dict)
def get_model_perf(
    model_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get performance metrics for a specific ML model
    """
    performance = get_model_performance(db, model_id)
    
    if not performance:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return performance
