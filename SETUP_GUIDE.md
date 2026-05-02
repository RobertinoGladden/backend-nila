# Aquaculture Backend - Setup & Deployment Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip/virtualenv
- Git

---

## Step 1: Clone & Setup Project

```bash
# Clone repository
git clone https://github.com/RobertinoGladden/backend-nila.git
cd backend-nila

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Database Setup

### 2a. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE aquaculture_db;

# Exit psql
\q
```

### 2b. Apply Migrations

```bash
# Apply existing sensor schema
psql -U postgres -d aquaculture_db -f init_db.sql

# Apply new user/farming/feed schema
psql -U postgres -d aquaculture_db -f migrations_add_user_features.sql

# Initialize ORM tables (creates tables from models)
python init_app_db.py
```

### 2c. Verify Tables

```bash
# List all tables
psql -U postgres -d aquaculture_db -c "\dt"

# Should see ~17 tables:
# - users, user_auth
# - farming_cycles, feed_stock, feed_transactions
# - feeding_schedule, feeding_history
# - sensor_data, predictions, alerts, notifications, actuators
# - ml_models, harvest_predictions, feeding_recommendations
# - sensor_calibrations, etc.
```

---

## Step 3: Configuration

### 3a. Update .env

```bash
# Edit .env file
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/aquaculture_db
SECRET_KEY=your-super-secret-key-change-this-min-32-chars
DEBUG=True  # Set to False in production
APP_HOST=0.0.0.0
APP_PORT=8000
```

### 3b. MQTT Setup (Optional)

If using MQTT for real-time sensors:

```env
MQTT_BROKER_HOST=broker.hivemq.com
MQTT_BROKER_PORT=1883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password
MQTT_CLIENT_ID=aquaculture-backend
```

---

## Step 4: Run Application

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verify Server is Running

```bash
# Check API is accessible
curl http://localhost:8000

# View API documentation
Open in browser: http://localhost:8000/docs
```

---

## Step 5: Test API

### 5a. Basic Health Check

```bash
curl http://localhost:8000
```

Expected response:
```json
{
  "service": "Aquaculture AI Backend",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs"
}
```

### 5b. Register User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "SecurePass123",
    "full_name": "John Farmer",
    "greenhouse_location": "Jakarta"
  }'
```

### 5c. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "SecurePass123"
  }'
```

### 5d. Get User Profile

```bash
# Replace TOKEN with actual access_token from login response
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer TOKEN"
```

### 5e. Create Farming Cycle

```bash
curl -X POST http://localhost:8000/farming-cycle/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cycle_name": "Cycle Januari 2024",
    "seeding_date": "2024-01-15"
  }'
```

---

## Step 6: Data Initialization (Optional)

### Add Sample Data

Create `seed_data.py`:

```python
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import MLModel

def seed_data():
    db = SessionLocal()
    try:
        # Check if models exist
        count = db.query(MLModel).count()
        if count > 0:
            print("Data already seeded!")
            return
        
        # Create ML models
        harvest_model = MLModel(
            model_type="harvest_estimation",
            model_version="v1.0",
            status="active",
            accuracy=85.0
        )
        
        feeding_model = MLModel(
            model_type="feeding_decision",
            model_version="v1.0",
            status="active",
            accuracy=80.0
        )
        
        db.add(harvest_model)
        db.add(feeding_model)
        db.commit()
        
        print("✅ Sample data created!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
```

Run seed:
```bash
python seed_data.py
```

---

## Step 7: Production Deployment

### 7a. Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn (4 workers)
gunicorn app.main:app -w 4 -b 0.0.0.0:8000 --timeout 120
```

### 7b. Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
      POSTGRES_DB: aquaculture_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres123@postgres:5432/aquaculture_db
      SECRET_KEY: your-secret-key
      DEBUG: "False"
    depends_on:
      - postgres
    volumes:
      - ./app:/app/app

volumes:
  postgres_data:
```

Run with Docker:
```bash
docker-compose up --build
```

---

## Troubleshooting

### Issue: Database Connection Failed

```
ERROR: (psycopg2.OperationalError) could not connect to server
```

**Solution:**
- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL in .env
- Verify database exists: `psql -U postgres -l`

### Issue: Import Errors

```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
- Make sure you're in the project root directory
- Run from correct Python environment: `which python`
- Install missing dependencies: `pip install -r requirements.txt`

### Issue: Port Already in Use

```
Address already in use
```

**Solution:**
- Run on different port: `uvicorn app.main:app --port 8001`
- Or kill existing process using port 8000

### Issue: MQTT Connection Error

```
WARNING MQTT gagal connect
```

**Solution:**
- MQTT is optional; app will work without it
- Check MQTT_BROKER_HOST and MQTT_BROKER_PORT in .env
- Verify internet connection to broker

---

## Monitoring

### Check Application Logs

```bash
# View recent logs (with follow)
tail -f app.log

# Search logs for errors
grep "ERROR" app.log
```

### Monitor Database

```bash
# Connect to database
psql -U postgres -d aquaculture_db

# Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# Check active connections
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;
```

---

## Performance Optimization

### 1. Database Indexes

Indexes are already created in migration. Verify:

```sql
SELECT indexname FROM pg_indexes WHERE schemaname='public' ORDER BY indexname;
```

### 2. Connection Pool

Adjust in `.env` or `database.py`:

```python
pool_size=10         # Number of connections to keep
max_overflow=20      # Additional connections allowed
pool_recycle=3600    # Recycle connections after 1 hour
```

### 3. API Rate Limiting

Add rate limiting to FastAPI app:

```bash
pip install slowapi
```

Then in `main.py`:

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## Security Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS (SSL/TLS)
- [ ] Rotate SECRET_KEY periodically
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted origins
- [ ] Implement rate limiting
- [ ] Monitor error logs for suspicious activity
- [ ] Regular database backups
- [ ] Keep dependencies updated

---

## Maintenance

### Backup Database

```bash
# Backup to file
pg_dump -U postgres aquaculture_db > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U postgres aquaculture_db < backup_20240115.sql
```

### Update Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package_name

# Update all packages
pip install --upgrade -r requirements.txt
```

### Database Maintenance

```bash
# Vacuum (clean up dead rows)
VACUUM ANALYZE;

# Check for missing indexes
SELECT schemaname, tablename FROM pg_tables WHERE schemaname != 'pg_catalog';
```

---

## Support & Documentation

- **API Docs**: http://localhost:8000/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **PostgreSQL**: https://www.postgresql.org/docs
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **JWT**: https://tools.ietf.org/html/rfc7519

---

## Next Steps

1. ✅ Setup complete!
2. Create ML models training pipeline
3. Integrate with frontend (Flutter/React)
4. Add webhook notifications
5. Setup automated backups
6. Deploy to production server
7. Configure monitoring and logging
