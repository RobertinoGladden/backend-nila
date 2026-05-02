# Aquaculture Backend - Complete API Documentation

## Overview

This is a comprehensive FastAPI backend system for greenhouse/aquaculture farming with user management, feed tracking, farming cycles, sensor integration, and ML-powered predictions.

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (with raw SQL queries via psycopg2)
- **Authentication**: JWT (José + Passlib with bcrypt)
- **ML**: scikit-learn + TensorFlow + pandas + numpy
- **Real-time**: MQTT (HiveMQ)

## Quick Start

### 1. Setup Database

```bash
# Apply migrations to create tables
psql -U postgres -d aquaculture_db -f migrations_add_user_features.sql

# Initialize app database (creates tables from ORM models)
python init_app_db.py
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/aquaculture_db
SECRET_KEY=your-secret-key-min-32-chars
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access API docs at: http://localhost:8000/docs

---

## Authentication Endpoints

### POST `/auth/register`
Register new user

**Request:**
```json
{
  "email": "farmer@example.com",
  "password": "SecurePass123",
  "full_name": "John Farmer",
  "phone_number": "+628123456789",
  "greenhouse_location": "Jakarta",
  "address": "Jl. Merdeka No. 1"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### POST `/auth/login`
Login with credentials

**Request:**
```json
{
  "email": "farmer@example.com",
  "password": "SecurePass123"
}
```

**Response:** Same as register

### GET `/auth/me`
Get current user profile

**Headers:** `Authorization: Bearer {access_token}`

**Response:**
```json
{
  "id": 1,
  "email": "farmer@example.com",
  "full_name": "John Farmer",
  "phone_number": "+628123456789",
  "greenhouse_location": "Jakarta",
  "address": "Jl. Merdeka No. 1",
  "profile_photo_url": null,
  "created_at": "2024-01-15T10:30:00"
}
```

### PUT `/auth/me`
Update user profile

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "full_name": "John Updated",
  "phone_number": "+628987654321",
  "greenhouse_location": "Bandung"
}
```

### POST `/auth/upload-photo`
Upload profile photo

**Headers:** 
- `Authorization: Bearer {access_token}`
- `Content-Type: multipart/form-data`

**Form Data:**
- `file`: Image file (jpg, png, etc.)

---

## Farming Cycle Endpoints

### POST `/farming-cycle/`
Start new farming cycle

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "cycle_name": "Cycle Januari 2024",
  "seeding_date": "2024-01-15"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "cycle_name": "Cycle Januari 2024",
  "seeding_date": "2024-01-15",
  "estimated_harvest_date": null,
  "actual_harvest_date": null,
  "status": "active",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### GET `/farming-cycle/`
List all farming cycles

**Headers:** `Authorization: Bearer {access_token}`

### GET `/farming-cycle/active`
Get active farming cycle

**Headers:** `Authorization: Bearer {access_token}`

### GET `/farming-cycle/{cycle_id}`
Get specific cycle details

### PUT `/farming-cycle/{cycle_id}`
Update farming cycle

**Request:**
```json
{
  "status": "completed",
  "actual_harvest_date": "2024-03-15"
}
```

### GET `/farming-cycle/{cycle_id}/days`
Get farming days elapsed

**Response:**
```json
{
  "cycle_id": 1,
  "farming_days": 45,
  "seeding_date": "2024-01-15",
  "status": "active"
}
```

### GET `/farming-cycle/{cycle_id}/stats`
Get cycle statistics

**Response:**
```json
{
  "cycle_id": 1,
  "farming_days": 45,
  "total_feeding_events": 135,
  "total_feed_quantity": 202.5,
  "feeding_schedules": 3,
  "seeding_date": "2024-01-15",
  "status": "active"
}
```

---

## Feed Management Endpoints

### GET `/feed/stocks`
Get all feed stocks

**Headers:** `Authorization: Bearer {access_token}`

### GET `/feed/stocks/{farming_cycle_id}`
Get feed stock for cycle

### POST `/feed/stocks/{stock_id}/transaction`
Record feed transaction (input or usage)

**Request:**
```json
{
  "transaction_type": "input",
  "quantity": 50.0,
  "notes": "Beli pakan 1 sak"
}
```

**Response:**
```json
{
  "id": 1,
  "feed_stock_id": 1,
  "transaction_type": "input",
  "quantity": 50.0,
  "notes": "Beli pakan 1 sak",
  "previous_quantity": 10.0,
  "new_quantity": 60.0,
  "created_at": "2024-01-15T11:00:00"
}
```

### GET `/feed/stocks/{stock_id}/history`
Get feed transaction history

**Query Params:**
- `limit`: Number of records (default: 100)

### GET `/feed/stocks/{stock_id}/stats`
Get feed statistics

**Response:**
```json
{
  "stock_id": 1,
  "current_quantity": 60.0,
  "unit": "kg",
  "total_input": 110.0,
  "total_usage": 50.0,
  "transaction_count": 5,
  "min_threshold": 20.0,
  "below_threshold": false
}
```

---

## Feeding Schedule Endpoints

### POST `/feed/schedule/{farming_cycle_id}`
Create feeding schedule

**Request:**
```json
{
  "scheduled_time": "07:00:00",
  "expected_quantity": 5.0,
  "frequency": "daily"
}
```

### GET `/feed/schedule/{farming_cycle_id}`
List feeding schedules for cycle

### POST `/feed/history/{farming_cycle_id}`
Record feeding event

**Request:**
```json
{
  "feeding_schedule_id": 1,
  "quantity_given": 5.2,
  "administered_by": "system",
  "notes": "Pagi feeding normal"
}
```

### GET `/feed/history/{farming_cycle_id}`
Get feeding history

### GET `/feed/history/{farming_cycle_id}/stats`
Get feeding statistics

**Response:**
```json
{
  "farming_cycle_id": 1,
  "total_feeding_events": 135,
  "total_feed_quantity": 202.5,
  "average_per_feeding": 1.5,
  "active_schedules": 3
}
```

---

## Machine Learning Endpoints

### POST `/ml/harvest-estimate/{farming_cycle_id}`
Generate harvest date prediction

**Headers:** `Authorization: Bearer {access_token}`

**Response:**
```json
{
  "id": 1,
  "farming_cycle_id": 1,
  "predicted_harvest_date": "2024-03-20",
  "confidence_score": 85.5,
  "ml_model_id": 1,
  "features_used": {
    "farming_days": 45,
    "avg_tds": 420.5,
    "avg_ph": 7.2,
    "avg_do": 6.8,
    "avg_temperature": 27.5,
    "total_feed_given": 202.5,
    "avg_feed_per_day": 4.5,
    "sensor_count": 180
  },
  "prediction_date": "2024-01-15T12:00:00"
}
```

### GET `/ml/harvest-estimate/{farming_cycle_id}`
Get all harvest predictions

**Query Params:**
- `limit`: Number of records (default: 10)

### POST `/ml/feeding-recommend/{farming_cycle_id}`
Get feeding recommendation

**Response:**
```json
{
  "id": 1,
  "farming_cycle_id": 1,
  "recommended_quantity": 4.8,
  "recommended_time": "07:00:00",
  "reasoning": "Based on water temp 27.5°C, DO 6.8 mg/L, and farming stage (45 days)",
  "confidence_score": 82.3,
  "ml_model_id": 2,
  "features_used": {
    "farming_days": 45,
    "current_temperature": 27.5,
    "current_do": 6.8,
    "recent_feed_total": 28.0,
    "recent_feeding_frequency": 3,
    "current_feed_stock": 60.0,
    "sensor_readings_count": 25
  },
  "recommendation_date": "2024-01-15T12:05:00"
}
```

### GET `/ml/feeding-recommend/{farming_cycle_id}`
Get recent feeding recommendations

### GET `/ml/models`
List active ML models

**Response:**
```json
{
  "harvest_estimation_model": {
    "id": 1,
    "version": "v1.0",
    "accuracy": 85.0
  },
  "feeding_decision_model": {
    "id": 2,
    "version": "v1.0",
    "accuracy": 80.0
  }
}
```

### GET `/ml/models/{model_id}/performance`
Get model performance metrics

---

## Sensor Endpoints (Existing)

### GET `/sensor-data/latest`
Get latest sensor reading

### POST `/sensor-data`
Record sensor data

### GET `/sensor-data/history`
Get historical sensor data

---

## Database Schema Overview

### Users & Authentication
- `users` - User profiles
- `user_auth` - Email/password credentials

### Farming
- `farming_cycles` - Farming periods and cycles
- `farming_cycle_id` - Links cycles to other entities

### Feed Management
- `feed_stock` - Current feed quantities
- `feed_transactions` - Feed input/usage history

### Feeding
- `feeding_schedule` - Planned feeding times
- `feeding_history` - Actual feeding records

### ML
- `ml_models` - Trained model metadata
- `harvest_predictions` - Predicted harvest dates
- `feeding_recommendations` - Feeding suggestions

### Sensors
- `sensor_data` - Raw sensor readings
- `sensor_calibrations` - Calibration records

---

## Error Handling

Standard HTTP status codes:
- `200` - Success
- `400` - Bad request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (access denied)
- `404` - Not found
- `500` - Server error

Error response format:
```json
{
  "detail": "Error message description"
}
```

---

## Authentication Flow

1. **Register** → Get tokens
2. **Login** → Get tokens
3. **Use access_token** in `Authorization: Bearer {token}` header
4. **Refresh token** when access_token expires (optional - can regenerate by re-login)

---

## Environment Variables

```
DATABASE_URL=postgresql://user:password@host:5432/aquaculture_db
SECRET_KEY=min-32-character-secret-key
AI_MODEL_PATH=ml/models/rf_classifier.pkl
MQTT_BROKER_HOST=broker.hivemq.com
MQTT_BROKER_PORT=1883
DEBUG=True
```

---

## Features Summary

✅ **User Management**: Register, login, profiles, photo upload
✅ **Farming Cycles**: Track seeding date → harvest
✅ **Feed Management**: Stock tracking, transactions, history
✅ **Feeding Schedules**: Plan and record feeding
✅ **Sensor Integration**: Real-time data collection
✅ **ML Predictions**: Harvest estimation, feeding recommendations
✅ **Water Quality**: AI-powered alerts and notifications
✅ **Actuator Control**: Aerator, heater, pump management
✅ **Real-time Updates**: MQTT integration

---

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Run integration tests:
```bash
pytest tests/integration/ -v
```

---

## Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to strong random string
- [ ] Set `DEBUG=False` in `.env`
- [ ] Use production PostgreSQL instance
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring and logging
- [ ] Database backups configured
- [ ] ML models trained on production data

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Support

For issues or questions, refer to:
- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy docs: https://docs.sqlalchemy.org
- PostgreSQL docs: https://www.postgresql.org/docs
