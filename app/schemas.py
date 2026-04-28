from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


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