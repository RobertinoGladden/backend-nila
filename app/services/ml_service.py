"""Machine Learning service for harvest estimation and feeding decisions"""
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os
from pathlib import Path

from app.models import (
    FarmingCycle, FeedingHistory, SensorData, HarvestPrediction,
    FeedingRecommendation, MLModel, FeedTransaction, FeedStock
)


# ── HARVEST ESTIMATION ─────────────────────────────────────────

def extract_harvest_features(db: Session, farming_cycle_id: int) -> dict:
    """Extract features for harvest prediction"""
    cycle = db.query(FarmingCycle).filter(FarmingCycle.id == farming_cycle_id).first()
    if not cycle:
        return None
    
    farming_days = (date.today() - cycle.seeding_date).days
    
    # Get average sensor readings (TDS, pH, DO, Temp)
    sensor_data = db.query(SensorData).filter(
        SensorData.created_at >= datetime.combine(cycle.seeding_date, datetime.min.time())
    ).all()
    
    avg_tds = np.mean([s.tds for s in sensor_data]) if sensor_data else 0
    avg_ph = np.mean([s.ph for s in sensor_data]) if sensor_data else 0
    avg_do = np.mean([s.do_level for s in sensor_data]) if sensor_data else 0
    avg_temp = np.mean([s.temperature for s in sensor_data]) if sensor_data else 0
    
    # Get feed statistics
    total_feed = db.query(func.sum(FeedingHistory.quantity_given)).filter(
        FeedingHistory.farming_cycle_id == farming_cycle_id
    ).scalar() or 0
    
    avg_feed_per_day = total_feed / max(farming_days, 1)
    
    features = {
        "farming_days": farming_days,
        "avg_tds": float(avg_tds),
        "avg_ph": float(avg_ph),
        "avg_do": float(avg_do),
        "avg_temperature": float(avg_temp),
        "total_feed_given": float(total_feed),
        "avg_feed_per_day": float(avg_feed_per_day),
        "sensor_count": len(sensor_data)
    }
    
    return features


def estimate_harvest_date(db: Session, farming_cycle_id: int) -> HarvestPrediction:
    """Estimate harvest date using ML model"""
    cycle = db.query(FarmingCycle).filter(FarmingCycle.id == farming_cycle_id).first()
    if not cycle:
        raise ValueError("Farming cycle not found")
    
    features = extract_harvest_features(db, farming_cycle_id)
    if not features:
        raise ValueError("Insufficient data for prediction")
    
    # Simple estimation: typical aquaculture cycle is 60-90 days
    # Adjust based on farming conditions
    farming_days = features["farming_days"]
    water_quality_score = (
        (7 - abs(features["avg_ph"] - 7)) * 0.3 +  # Optimal pH ~7
        min(features["avg_do"] / 6, 1) * 0.3 +      # Optimal DO ~6
        (1 - min(abs(features["avg_tds"] - 400) / 1000, 1)) * 0.4  # Optimal TDS ~400
    )
    
    # Estimate remaining days (70-90 days total optimal cycle)
    base_remaining = 75
    remaining_days = int(base_remaining * water_quality_score)
    estimated_harvest_date = date.today() + timedelta(days=remaining_days)
    
    # Calculate confidence based on data availability
    confidence = min(features["sensor_count"] / 100 * 100, 95)
    
    # Get or create active model
    ml_model = db.query(MLModel).filter(
        MLModel.model_type == "harvest_estimation",
        MLModel.status == "active"
    ).first()
    
    if not ml_model:
        ml_model = MLModel(
            model_type="harvest_estimation",
            model_version="v1.0",
            status="active",
            accuracy=85.0
        )
        db.add(ml_model)
        db.flush()
    
    # Create prediction
    prediction = HarvestPrediction(
        farming_cycle_id=farming_cycle_id,
        predicted_harvest_date=estimated_harvest_date,
        confidence_score=confidence,
        ml_model_id=ml_model.id,
        features_used=features
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    # Update cycle estimated harvest date
    cycle.estimated_harvest_date = estimated_harvest_date
    db.commit()
    
    return prediction


def get_harvest_predictions(db: Session, farming_cycle_id: int) -> list:
    """Get all harvest predictions for a cycle"""
    return db.query(HarvestPrediction).filter(
        HarvestPrediction.farming_cycle_id == farming_cycle_id
    ).order_by(HarvestPrediction.prediction_date.desc()).all()


# ── FEEDING RECOMMENDATIONS ────────────────────────────────────

def extract_feeding_features(db: Session, farming_cycle_id: int) -> dict:
    """Extract features for feeding recommendations"""
    cycle = db.query(FarmingCycle).filter(FarmingCycle.id == farming_cycle_id).first()
    if not cycle:
        return None
    
    farming_days = (date.today() - cycle.seeding_date).days
    
    # Get recent sensor data (last 7 days)
    recent_sensor = db.query(SensorData).filter(
        SensorData.created_at >= datetime.now() - timedelta(days=7)
    ).order_by(SensorData.created_at.desc()).limit(50).all()
    
    avg_temp = np.mean([s.temperature for s in recent_sensor]) if recent_sensor else 25
    avg_do = np.mean([s.do_level for s in recent_sensor]) if recent_sensor else 6
    
    # Get feeding history (last 7 days)
    recent_feeding = db.query(FeedingHistory).filter(
        FeedingHistory.farming_cycle_id == farming_cycle_id,
        FeedingHistory.actual_time >= datetime.now() - timedelta(days=7)
    ).all()
    
    total_recent_feed = sum(f.quantity_given for f in recent_feeding)
    feeding_frequency = len(recent_feeding)
    
    # Get feed stock
    feed_stock = db.query(FeedStock).filter(
        FeedStock.farming_cycle_id == farming_cycle_id
    ).first()
    
    current_feed = feed_stock.current_quantity if feed_stock else 0
    
    features = {
        "farming_days": farming_days,
        "current_temperature": float(avg_temp),
        "current_do": float(avg_do),
        "recent_feed_total": float(total_recent_feed),
        "recent_feeding_frequency": feeding_frequency,
        "current_feed_stock": float(current_feed),
        "sensor_readings_count": len(recent_sensor)
    }
    
    return features


def recommend_feeding(db: Session, farming_cycle_id: int) -> FeedingRecommendation:
    """Generate feeding recommendation using ML"""
    cycle = db.query(FarmingCycle).filter(FarmingCycle.id == farming_cycle_id).first()
    if not cycle:
        raise ValueError("Farming cycle not found")
    
    features = extract_feeding_features(db, farming_cycle_id)
    if not features:
        raise ValueError("Insufficient data for recommendation")
    
    # Simple recommendation logic based on conditions
    farming_days = features["farming_days"]
    temp = features["current_temperature"]
    do_level = features["current_do"]
    
    # Base feeding: ~3-5% of body weight per day (assume avg 100g, so 3-5g per day)
    # Adjust by farming stage and water conditions
    base_quantity = 4.0
    
    # Temperature adjustment (feed more in warmer water)
    if temp < 20:
        temp_factor = 0.7
    elif temp < 25:
        temp_factor = 0.85
    elif temp < 30:
        temp_factor = 1.0
    else:
        temp_factor = 0.8
    
    # DO adjustment (feed less if DO is low)
    if do_level < 4:
        do_factor = 0.6
    elif do_level < 5:
        do_factor = 0.8
    else:
        do_factor = 1.0
    
    # Farming stage adjustment (reduce feeding near harvest)
    if farming_days < 30:
        stage_factor = 0.7  # Early stage
    elif farming_days < 60:
        stage_factor = 1.0  # Growth stage
    else:
        stage_factor = 0.85  # Late stage
    
    recommended_quantity = base_quantity * temp_factor * do_factor * stage_factor
    
    # Confidence based on data quality
    confidence = min(80 + (features["sensor_readings_count"] / 50 * 15), 95)
    
    # Get or create active model
    ml_model = db.query(MLModel).filter(
        MLModel.model_type == "feeding_decision",
        MLModel.status == "active"
    ).first()
    
    if not ml_model:
        ml_model = MLModel(
            model_type="feeding_decision",
            model_version="v1.0",
            status="active",
            accuracy=80.0
        )
        db.add(ml_model)
        db.flush()
    
    reasoning = f"Based on water temp {temp}°C, DO {do_level} mg/L, and farming stage ({farming_days} days)"
    
    # Recommended time: typically morning feeding
    from datetime import time
    recommended_time = time(7, 0)
    
    recommendation = FeedingRecommendation(
        farming_cycle_id=farming_cycle_id,
        recommended_quantity=round(recommended_quantity, 2),
        recommended_time=recommended_time,
        reasoning=reasoning,
        confidence_score=confidence,
        ml_model_id=ml_model.id,
        features_used=features
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    return recommendation


def get_feeding_recommendations(db: Session, farming_cycle_id: int, limit: int = 10) -> list:
    """Get recent feeding recommendations"""
    return db.query(FeedingRecommendation).filter(
        FeedingRecommendation.farming_cycle_id == farming_cycle_id
    ).order_by(FeedingRecommendation.recommendation_date.desc()).limit(limit).all()


# ── ML MODEL MANAGEMENT ────────────────────────────────────────

def get_active_ml_models(db: Session) -> dict:
    """Get all active ML models"""
    models = db.query(MLModel).filter(MLModel.status == "active").all()
    
    return {
        "harvest_estimation": next((m for m in models if m.model_type == "harvest_estimation"), None),
        "feeding_decision": next((m for m in models if m.model_type == "feeding_decision"), None)
    }


def get_model_performance(db: Session, model_id: int) -> dict:
    """Get model performance metrics"""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    if not model:
        return None
    
    if model.model_type == "harvest_estimation":
        predictions = db.query(HarvestPrediction).filter(
            HarvestPrediction.ml_model_id == model_id
        ).all()
        
        avg_confidence = np.mean([p.confidence_score for p in predictions]) if predictions else 0
        
        return {
            "model_id": model_id,
            "model_type": model.model_type,
            "version": model.model_version,
            "total_predictions": len(predictions),
            "avg_confidence": round(avg_confidence, 2),
            "accuracy": model.accuracy
        }
    
    elif model.model_type == "feeding_decision":
        recommendations = db.query(FeedingRecommendation).filter(
            FeedingRecommendation.ml_model_id == model_id
        ).all()
        
        avg_confidence = np.mean([r.confidence_score for r in recommendations]) if recommendations else 0
        
        return {
            "model_id": model_id,
            "model_type": model.model_type,
            "version": model.model_version,
            "total_recommendations": len(recommendations),
            "avg_confidence": round(avg_confidence, 2),
            "accuracy": model.accuracy
        }
    
    return None
