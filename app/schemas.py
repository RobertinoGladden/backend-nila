from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from enum import Enum


# ── ENUMS ──────────────────────────────────────────────────────

class FarmingCycleStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    HARVESTING = "harvesting"
    COMPLETED = "completed"


class TransactionType(str, Enum):
    INPUT = "input"
    USAGE = "usage"


# ── USER MANAGEMENT SCHEMAS ────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    full_name: str
    phone_number: Optional[str] = None
    greenhouse_location: Optional[str] = None
    address: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "farmer@example.com",
                "password": "securepass123",
                "full_name": "John Doe",
                "phone_number": "+628123456789",
                "greenhouse_location": "Jakarta",
                "address": "Jl. Merdeka No. 1"
            }
        }
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone_number: Optional[str] = None
    greenhouse_location: Optional[str] = None
    address: Optional[str] = None
    profile_photo_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    greenhouse_location: Optional[str] = None
    address: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


# ── FARMING CYCLE SCHEMAS ──────────────────────────────────────

class FarmingCycleCreate(BaseModel):
    cycle_name: Optional[str] = None
    seeding_date: date


class FarmingCycleResponse(BaseModel):
    id: int
    user_id: int
    cycle_name: Optional[str]
    seeding_date: date
    estimated_harvest_date: Optional[date]
    actual_harvest_date: Optional[date]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FarmingCycleUpdate(BaseModel):
    cycle_name: Optional[str] = None
    status: Optional[FarmingCycleStatus] = None
    actual_harvest_date: Optional[date] = None


# ── FEED MANAGEMENT SCHEMAS ────────────────────────────────────

class FeedStockCreate(BaseModel):
    farming_cycle_id: Optional[int] = None
    current_quantity: float
    unit: str = "kg"
    min_threshold: Optional[float] = None


class FeedStockResponse(BaseModel):
    id: int
    user_id: int
    farming_cycle_id: Optional[int]
    current_quantity: float
    unit: str
    min_threshold: Optional[float]
    updated_at: datetime

    model_config = {"from_attributes": True}


class FeedTransactionCreate(BaseModel):
    transaction_type: TransactionType
    quantity: float = Field(..., gt=0)
    notes: Optional[str] = None


class FeedTransactionResponse(BaseModel):
    id: int
    feed_stock_id: int
    transaction_type: str
    quantity: float
    notes: Optional[str]
    previous_quantity: Optional[float]
    new_quantity: Optional[float]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── FEEDING SCHEDULE SCHEMAS ───────────────────────────────────

class FeedingScheduleCreate(BaseModel):
    scheduled_time: time
    expected_quantity: float = Field(..., gt=0)
    frequency: str = "daily"


class FeedingScheduleResponse(BaseModel):
    id: int
    farming_cycle_id: int
    scheduled_time: time
    expected_quantity: float
    frequency: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedingHistoryCreate(BaseModel):
    feeding_schedule_id: Optional[int] = None
    quantity_given: float = Field(..., gt=0)
    administered_by: str = "system"
    notes: Optional[str] = None


class FeedingHistoryResponse(BaseModel):
    id: int
    feeding_schedule_id: Optional[int]
    farming_cycle_id: int
    actual_time: datetime
    quantity_given: float
    administered_by: str
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── SENSOR SCHEMAS ─────────────────────────────────────────────

class SensorCalibrationCreate(BaseModel):
    farming_cycle_id: Optional[int] = None
    sensor_type: str
    calibration_value: float
    reference_value: float
    notes: Optional[str] = None


class SensorCalibrationResponse(BaseModel):
    id: int
    farming_cycle_id: Optional[int]
    sensor_type: str
    calibration_date: datetime
    calibration_value: float
    reference_value: float
    status: str
    notes: Optional[str]

    model_config = {"from_attributes": True}


# ── ML SCHEMAS ─────────────────────────────────────────────────

class HarvestPredictionResponse(BaseModel):
    id: int
    farming_cycle_id: int
    predicted_harvest_date: date
    confidence_score: Optional[float]
    ml_model_id: Optional[int]
    features_used: Optional[Dict[str, Any]]
    prediction_date: datetime

    model_config = {"from_attributes": True}


class FeedingRecommendationResponse(BaseModel):
    id: int
    farming_cycle_id: int
    recommended_quantity: float
    recommended_time: Optional[time]
    reasoning: Optional[str]
    confidence_score: Optional[float]
    ml_model_id: Optional[int]
    features_used: Optional[Dict[str, Any]]
    recommendation_date: datetime

    model_config = {"from_attributes": True}


# ── SENSOR DATA ───────────────────────────────────────────────

class SensorDataCreate(BaseModel):
    device_id:   str   = Field(default="sensor-01")
    tds:         float = Field(..., ge=0, le=5000)
    ph:          float = Field(..., ge=0, le=14)
    do_level:    float = Field(..., ge=0, le=20)
    temperature: float = Field(..., ge=0, le=50)
    turbidity:   float = Field(default=0, ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "device_id":   "sensor-01",
                "tds":         450.5,
                "ph":          7.8,
                "do_level":    6.5,
                "temperature": 27.5,
                "turbidity":   3.1
            }
        }
    }


class SensorDataResponse(BaseModel):
    id:          int
    device_id:   str
    tds:         float
    ph:          float
    do_level:    float
    temperature: float
    turbidity:   float
    created_at:  datetime

    model_config = {"from_attributes": True}


# ── PREDICTIONS ───────────────────────────────────────────────

class PredictionResponse(BaseModel):
    id:             int
    sensor_data_id: int
    status:         str
    confidence:     float
    prob_normal:    float
    prob_waspada:   float
    prob_kritis:    float
    urgency:        str
    model_version:  str
    created_at:     datetime

    model_config = {"from_attributes": True}


# ── ALERTS ────────────────────────────────────────────────────

class AlertResponse(BaseModel):
    id:             int
    sensor_data_id: int
    prediction_id:  Optional[int]
    level:          str
    message:        str
    action:         Optional[str]
    status:         str
    created_at:     datetime
    resolved_at:    Optional[datetime]

    model_config = {"from_attributes": True}


# ── NOTIFICATIONS ─────────────────────────────────────────────

class NotificationResponse(BaseModel):
    id:         int
    alert_id:   int
    title:      str
    message:    str
    is_read:    bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── ACTUATOR ──────────────────────────────────────────────────

class ActuatorControlRequest(BaseModel):
    device_name:  str = Field(..., description="aerator / heater / pompa")
    action:       str = Field(..., description="on / off")
    triggered_by: str = Field(default="manual")

    @field_validator("device_name")
    @classmethod
    def validate_device(cls, v):
        allowed = ["aerator", "heater", "pompa"]
        if v not in allowed:
            raise ValueError(f"device_name harus salah satu dari: {allowed}")
        return v

    @field_validator("action")
    @classmethod
    def validate_action(cls, v):
        if v not in ["on", "off"]:
            raise ValueError("action harus 'on' atau 'off'")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "device_name":  "aerator",
                "action":       "on",
                "triggered_by": "manual"
            }
        }
    }


class ActuatorStatusResponse(BaseModel):
    id:          int
    device_name: str
    is_active:   bool
    mode:        str
    updated_at:  datetime

    model_config = {"from_attributes": True}


class ActuatorLogResponse(BaseModel):
    id:           int
    device_name:  str
    action:       str
    triggered_by: str
    alert_id:     Optional[int]
    created_at:   datetime

    model_config = {"from_attributes": True}


# ── AI PREDICT ────────────────────────────────────────────────

class PredictRequest(BaseModel):
    tds:         float
    ph:          float
    do_level:    float
    temperature: float
    turbidity:   float = 0.0

    model_config = {
        "json_schema_extra": {
            "example": {
                "tds":         450.5,
                "ph":          7.8,
                "do_level":    6.5,
                "temperature": 27.5,
                "turbidity":   3.1
            }
        }
    }


class PredictResponse(BaseModel):
    status:      str
    confidence:  float
    urgency:     str
    action:      str
    probability: dict


# ── DASHBOARD ─────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    latest_sensor:              Optional[SensorDataResponse]
    latest_prediction:          Optional[PredictionResponse]
    active_alerts_count:        int
    unread_notifications_count: int
    actuator_status:            List[ActuatorStatusResponse]