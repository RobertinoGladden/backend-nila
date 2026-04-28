from sqlalchemy import (
    Column, Integer, Float, String,
    Boolean, Text, TIMESTAMP, ForeignKey, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id          = Column(Integer, primary_key=True, index=True)
    device_id   = Column(String(50), default="sensor-01")
    tds         = Column(Float, nullable=False)
    ph          = Column(Float, nullable=False)
    do_level    = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    turbidity   = Column(Float, default=0)
    created_at  = Column(TIMESTAMP, server_default=func.now())

    predictions = relationship("Prediction", back_populates="sensor_data")
    alerts      = relationship("Alert", back_populates="sensor_data")


class Prediction(Base):
    __tablename__ = "predictions"

    id             = Column(Integer, primary_key=True, index=True)
    sensor_data_id = Column(Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"))
    status         = Column(String(10), nullable=False)
    confidence     = Column(Float, nullable=False)
    prob_normal    = Column(Float, default=0)
    prob_waspada   = Column(Float, default=0)
    prob_kritis    = Column(Float, default=0)
    urgency        = Column(String(10), default="low")
    model_version  = Column(String(20), default="RF-v1")
    created_at     = Column(TIMESTAMP, server_default=func.now())

    sensor_data = relationship("SensorData", back_populates="predictions")
    alerts      = relationship("Alert", back_populates="prediction")


class Alert(Base):
    __tablename__ = "alerts"

    id             = Column(Integer, primary_key=True, index=True)
    sensor_data_id = Column(Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"))
    prediction_id  = Column(Integer, ForeignKey("predictions.id", ondelete="SET NULL"), nullable=True)
    level          = Column(String(10), nullable=False)
    message        = Column(Text, nullable=False)
    action         = Column(Text, nullable=True)
    status         = Column(String(10), default="active")
    created_at     = Column(TIMESTAMP, server_default=func.now())
    resolved_at    = Column(TIMESTAMP, nullable=True)

    sensor_data   = relationship("SensorData", back_populates="alerts")
    prediction    = relationship("Prediction", back_populates="alerts")
    notifications = relationship("Notification", back_populates="alert")
    actuator_logs = relationship("ActuatorLog", back_populates="alert")


class Notification(Base):
    __tablename__ = "notifications"

    id         = Column(Integer, primary_key=True, index=True)
    alert_id   = Column(Integer, ForeignKey("alerts.id", ondelete="CASCADE"))
    title      = Column(String(100), nullable=False)
    message    = Column(Text, nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    alert = relationship("Alert", back_populates="notifications")


class ActuatorStatus(Base):
    __tablename__ = "actuator_status"

    id          = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(50), unique=True, nullable=False)
    is_active   = Column(Boolean, default=False)
    mode        = Column(String(10), default="auto")
    updated_at  = Column(TIMESTAMP, server_default=func.now())


class ActuatorLog(Base):
    __tablename__ = "actuator_logs"

    id           = Column(Integer, primary_key=True, index=True)
    device_name  = Column(String(50), nullable=False)
    action       = Column(String(10), nullable=False)
    triggered_by = Column(String(20), default="manual")
    alert_id     = Column(Integer, ForeignKey("alerts.id", ondelete="SET NULL"), nullable=True)
    created_at   = Column(TIMESTAMP, server_default=func.now())

    alert = relationship("Alert", back_populates="actuator_logs")