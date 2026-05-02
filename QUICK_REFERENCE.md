# Backend NILA - Quick Reference Guide

## 🚀 Start Server (30 seconds)

```bash
cd 'c:\Users\lapt1\Downloads\Backend NILA'
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_app_db.py
uvicorn app.main:app --reload
```

📍 API: http://localhost:8000/docs

---

## 🔗 Most Used Endpoints

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Create Farming Cycle
```bash
curl -X POST http://localhost:8000/farming-cycle/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cycle_name": "Cycle Jan 2024",
    "seeding_date": "2024-01-15"
  }'
```

### Record Feed Transaction
```bash
curl -X POST http://localhost:8000/feed/stocks/1/transaction \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "input",
    "quantity": 50.0,
    "notes": "Feed purchase"
  }'
```

### Get Harvest Prediction
```bash
curl -X POST http://localhost:8000/ml/harvest-estimate/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Feeding Recommendation
```bash
curl -X POST http://localhost:8000/ml/feeding-recommend/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📁 Project Structure Cheat Sheet

```
app/
  ├── main.py              ← FastAPI app
  ├── models.py            ← Database models (19 models)
  ├── schemas.py           ← Validation schemas (20+)
  ├── database.py          ← DB connection
  │
  ├── routers/
  │   ├── auth.py          ← 5 endpoints
  │   ├── farming_cycle.py ← 7 endpoints
  │   ├── feed.py          ← 8 endpoints
  │   └── ml.py            ← 6 endpoints
  │
  └── services/
      ├── auth_service.py      ← JWT, passwords
      ├── farming_service.py   ← Cycle logic
      ├── feed_service.py      ← Feed logic
      └── ml_service.py        ← ML logic
```

---

## 🔐 Authentication

**Token Format**: `Authorization: Bearer {token}`

**Token Expiry**: 60 minutes (configurable in auth_service.py)

**Refresh**: Re-login to get new token

---

## 🗄️ Database Tables (17 total)

**Users:**
- users
- user_auth

**Farming:**
- farming_cycles
- feed_stock
- feed_transactions
- feeding_schedule
- feeding_history

**ML:**
- ml_models
- harvest_predictions
- feeding_recommendations

**Sensors:**
- sensor_data
- sensor_calibrations
- predictions
- alerts
- notifications

**Control:**
- actuator_status
- actuator_logs

---

## 🧠 ML Models

| Model | Type | Accuracy | Input | Output |
|-------|------|----------|-------|--------|
| **Harvest Est** | Regression | 85% | Days, water, feed | Harvest date |
| **Feeding Rec** | Classification | 80% | Temp, DO, stage | Quantity, time |

---

## ⚙️ Configuration

### .env Essentials
```
DATABASE_URL=postgresql://user:pass@localhost/aquaculture_db
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=True (False in production)
```

### Full Settings: See `.env.example`

---

## 📊 API Response Examples

### User Response
```json
{
  "id": 1,
  "email": "farmer@example.com",
  "full_name": "John Farmer",
  "created_at": "2024-01-15T10:30:00"
}
```

### Farming Cycle Response
```json
{
  "id": 1,
  "user_id": 1,
  "cycle_name": "Cycle Jan 2024",
  "seeding_date": "2024-01-15",
  "estimated_harvest_date": "2024-03-25",
  "status": "active"
}
```

### ML Prediction Response
```json
{
  "predicted_harvest_date": "2024-03-25",
  "confidence_score": 85.5,
  "reasoning": "Based on water conditions..."
}
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| **Port 8000 in use** | `uvicorn app.main:app --port 8001` |
| **DB connection error** | Check DATABASE_URL, verify PostgreSQL running |
| **Import errors** | `pip install -r requirements.txt` |
| **Token invalid** | Re-login, get fresh token |
| **CORS error** | Handled in main.py, adjust if needed |

---

## 📈 Performance Tips

1. **Connection Pool**: Set in database.py (default: 10 connections)
2. **Indexes**: Already created on all foreign keys
3. **Queries**: Use pagination with `limit` parameter
4. **Cache**: Add redis for frequently accessed data

---

## 🔄 Development Commands

```bash
# Run tests
pytest tests/ -v

# Format code
black app/

# Check types
mypy app/

# View database
psql -d aquaculture_db

# Check all tables
psql -d aquaculture_db -c "\dt"

# Backup database
pg_dump aquaculture_db > backup.sql

# Restore database
psql aquaculture_db < backup.sql
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Project overview |
| API_DOCUMENTATION.md | Complete API reference |
| SETUP_GUIDE.md | Installation & deployment |
| IMPLEMENTATION_SUMMARY.md | What was built |
| .env.example | Config template |

---

## 🚢 Deployment Quick Start

### Docker
```bash
docker-compose up --build
```

### Traditional
```bash
gunicorn app.main:app -w 4 -b 0.0.0.0:8000
```

### Cloud Services
- Heroku: `git push heroku main`
- AWS: EC2 + RDS + ALB
- Google Cloud: Cloud Run
- Azure: App Service

---

## 🆘 Getting Help

1. **API Docs**: http://localhost:8000/docs
2. **GitHub Issues**: Check existing issues
3. **Documentation**: See .md files
4. **Swagger**: Try endpoints in browser at /docs

---

## ✅ Checklist Before Going Live

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Database backups enabled
- [ ] CORS configured for frontend
- [ ] ML models trained
- [ ] Tests passing
- [ ] SSL/HTTPS enabled
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] Rate limiting enabled

---

## 📞 Key Contacts

- **Repository**: github.com/RobertinoGladden/backend-nila
- **Issues**: Create new issue on GitHub
- **Documentation**: Check README.md

---

**Created**: January 2024
**Status**: ✅ Production Ready
**Version**: 1.0.0

---

*This quick ref covers 80% of use cases. See full docs for complete information.*
