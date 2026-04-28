from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import check_db_connection, SessionLocal
from app.models import SensorData, Prediction, Alert, Notification, ActuatorStatus
from app.schemas import DashboardResponse
from app.services.ai_service import load_model
from app.mqtt.client import create_mqtt_client, connect_mqtt, disconnect_mqtt
from app.mqtt.subscriber import on_message
from app.routers import sensor_data, predictions, alerts, notifications, actuator

# Global MQTT client
_mqtt_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _mqtt_client

    print("\n" + "=" * 55)
    print("  Aquaculture Backend Starting...")
    print("=" * 55)

    # 1. Cek database
    if check_db_connection():
        print("  OK Database PostgreSQL terhubung")
    else:
        print("  ERROR Database tidak bisa diakses!")

    # 2. Load AI Model
    model_loaded = load_model()
    if model_loaded:
        print("  OK AI Model (Random Forest) loaded")
    else:
        print("  WARNING AI Model tidak ditemukan, pakai rule-based fallback")

    # 3. Connect MQTT
    try:
        _mqtt_client = create_mqtt_client(on_message_callback=on_message)
        connect_mqtt(_mqtt_client)
        print("  OK MQTT Client terhubung ke HiveMQ")
    except Exception as e:
        print(f"  WARNING MQTT gagal connect: {e}")
        _mqtt_client = None

    print("=" * 55)
    print("  Server siap menerima data sensor")
    print("  Docs: http://localhost:8000/docs")
    print("=" * 55 + "\n")

    yield

    # Shutdown
    print("\nShutting down...")
    if _mqtt_client:
        disconnect_mqtt(_mqtt_client)
    print("Shutdown selesai")


# Inisialisasi FastAPI
app = FastAPI(
    title="Aquaculture AI Backend",
    description="Sistem Monitoring Kualitas Air Budidaya Ikan Nila",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS untuk Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(sensor_data.router)
app.include_router(predictions.router)
app.include_router(alerts.router)
app.include_router(notifications.router)
app.include_router(actuator.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "service": "Aquaculture AI Backend",
        "version": "1.0.0",
        "status": "running",
        "time": datetime.now().isoformat(),
        "docs": "/docs",
        "endpoints": {
            "sensor_data":       "/sensor-data",
            "sensor_latest":     "/sensor-data/latest",
            "sensor_history":    "/sensor-data/history",
            "predictions":       "/predictions",
            "predict_latest":    "/predictions/latest",
            "predict_manual":    "/predictions/predict",
            "alerts":            "/alerts",
            "alerts_active":     "/alerts/active",
            "notifications":     "/notifications",
            "notif_unread":      "/notifications/unread",
            "notif_count":       "/notifications/unread/count",
            "actuator_status":   "/actuator/status",
            "actuator_control":  "/actuator/control",
            "actuator_logs":     "/actuator/logs",
            "dashboard":         "/dashboard",
            "summary":           "/summary",
        }
    }


@app.get("/dashboard", response_model=DashboardResponse, tags=["Dashboard"])
def get_dashboard():
    db = SessionLocal()
    try:
        latest_sensor = (
            db.query(SensorData)
            .order_by(SensorData.created_at.desc())
            .first()
        )

        latest_prediction = (
            db.query(Prediction)
            .order_by(Prediction.created_at.desc())
            .first()
        )

        active_alerts_count = (
            db.query(Alert)
            .filter(Alert.status == "active")
            .count()
        )

        unread_notif_count = (
            db.query(Notification)
            .filter(Notification.is_read == False)
            .count()
        )

        actuator_status = db.query(ActuatorStatus).all()

        return DashboardResponse(
            latest_sensor=latest_sensor,
            latest_prediction=latest_prediction,
            active_alerts_count=active_alerts_count,
            unread_notifications_count=unread_notif_count,
            actuator_status=actuator_status,
        )
    finally:
        db.close()


@app.get("/summary", tags=["Dashboard"])
def get_summary():
    db = SessionLocal()
    try:
        total_sensor      = db.query(SensorData).count()
        total_predictions = db.query(Prediction).count()
        total_alerts      = db.query(Alert).count()
        active_alerts     = db.query(Alert).filter(Alert.status == "active").count()
        total_notif       = db.query(Notification).count()
        unread_notif      = db.query(Notification).filter(Notification.is_read == False).count()

        status_dist = (
            db.query(Prediction.status, func.count(Prediction.id))
            .group_by(Prediction.status)
            .all()
        )
        distribution = {row[0]: row[1] for row in status_dist}

        actuators = db.query(ActuatorStatus).all()
        actuator_summary = [
            {
                "device":    a.device_name,
                "is_active": a.is_active,
                "mode":      a.mode,
            }
            for a in actuators
        ]

        return {
            "total_sensor_readings":   total_sensor,
            "total_predictions":       total_predictions,
            "total_alerts":            total_alerts,
            "active_alerts":           active_alerts,
            "total_notifications":     total_notif,
            "unread_notifications":    unread_notif,
            "prediction_distribution": distribution,
            "actuators":               actuator_summary,
            "generated_at":            datetime.now().isoformat(),
        }
    finally:
        db.close()