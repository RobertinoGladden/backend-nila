# Aquaculture Monitoring & Management Backend (Backend NILA)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Comprehensive backend system for aquaculture farming with AI-powered predictions, real-time monitoring, and intelligent feed management.

## 🎯 Features

### Core Features
- ✅ **User Management** - Secure registration, login, profile management
- ✅ **Farming Cycles** - Track complete farming lifecycle from seeding to harvest
- ✅ **Feed Management** - Real-time stock tracking, transaction history
- ✅ **Feeding Schedules** - Automated and manual feeding tracking
- ✅ **Water Quality Monitoring** - Real-time sensor data (TDS, pH, DO, Temperature)
- ✅ **AI Predictions** - ML models for harvest estimation and feeding optimization
- ✅ **Sensor Calibration** - Automatic sensor calibration system
- ✅ **Alerts & Notifications** - Real-time alerts for abnormal conditions
- ✅ **Actuator Control** - Manage aerators, heaters, pumps
- ✅ **MQTT Integration** - Real-time IoT data streaming

### Advanced Features
- 🤖 **Harvest Estimation ML** - Predict harvest date based on conditions
- 🤖 **Feeding Optimization ML** - Recommend optimal feeding quantity & timing
- 📊 **Analytics Dashboard** - Comprehensive statistics and insights
- 📱 **Mobile API** - RESTful API for Flutter/React apps
- 🔐 **JWT Authentication** - Secure token-based auth
- 📡 **Real-time Updates** - MQTT pub/sub for live data
- 🔄 **Auto-scaling** - Connection pooling, query optimization

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
│            (Flutter/React Native App)                       │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API / WebSocket
┌────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Routers: Auth, Farming, Feed, ML, Sensors             │ │
│  │ Services: Business Logic & ML Models                  │ │
│  │ Database: SQLAlchemy ORM + Raw SQL                    │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌───▼────┐
    │PostgreSQL│ │ MQTT   │ │Storage │
    │Database  │ │ Broker │ │ (Files)│
    └──────────┘ └────────┘ └────────┘
```

## 📁 Project Structure

```
backend-nila/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # Database connection & setup
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic validation schemas
│   ├── routers/
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── farming_cycle.py    # Farming cycle endpoints
│   │   ├── feed.py             # Feed management endpoints
│   │   ├── ml.py               # ML prediction endpoints
│   │   ├── sensor_data.py      # Sensor endpoints (existing)
│   │   ├── predictions.py      # AI predictions (existing)
│   │   ├── alerts.py           # Alerts (existing)
│   │   ├── notifications.py    # Notifications (existing)
│   │   └── actuator.py         # Actuator control (existing)
│   ├── services/
│   │   ├── auth_service.py     # JWT & password handling
│   │   ├── farming_service.py  # Farming cycle logic
│   │   ├── feed_service.py     # Feed management logic
│   │   ├── ml_service.py       # ML models & predictions
│   │   ├── ai_service.py       # Water quality AI (existing)
│   │   └── mqtt_service.py     # MQTT integration (existing)
│   ├── mqtt/
│   │   ├── client.py           # MQTT client setup
│   │   └── subscriber.py       # Message handlers
│   └── uploads/                # File uploads directory
├── ml/
│   ├── models/
│   │   ├── rf_classifier.pkl   # Water quality model
│   │   ├── scaler.pkl          # Data normalization
│   │   └── label_encoder.pkl   # Label encoding
│   ├── training/
│   │   └── train_models.py     # Model training pipeline
│   └── data/
│       └── historical_data.csv # Training data
├── tests/
│   ├── test_auth.py
│   ├── test_farming.py
│   ├── test_feed.py
│   └── test_ml.py
├── .env                        # Environment variables
├── .env.example                # Example env template
├── requirements.txt            # Python dependencies
├── init_db.sql                 # Database schema (existing)
├── migrations_add_user_features.sql  # New schema additions
├── init_app_db.py              # ORM table initialization
├── API_DOCUMENTATION.md        # Complete API docs
├── SETUP_GUIDE.md              # Setup & deployment guide
└── README.md                   # This file
```

## 🔧 Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI 0.111+ |
| **Database** | PostgreSQL 15+ |
| **ORM** | SQLAlchemy 2.0+ |
| **Auth** | JWT + Passlib (bcrypt) |
| **ML** | scikit-learn, TensorFlow |
| **Data** | pandas, numpy |
| **Real-time** | MQTT (HiveMQ) |
| **Server** | Uvicorn, Gunicorn |
| **Testing** | pytest |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/RobertinoGladden/backend-nila.git
cd backend-nila

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
psql -U postgres -f init_db.sql
psql -U postgres -d aquaculture_db -f migrations_add_user_features.sql
python init_app_db.py

# 5. Configure .env
cp .env.example .env
# Edit .env with your settings

# 6. Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation**: http://localhost:8000/docs

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /auth/me` - Get profile
- `PUT /auth/me` - Update profile
- `POST /auth/upload-photo` - Upload photo

### Farming Cycles
- `POST /farming-cycle/` - Start new cycle
- `GET /farming-cycle/` - List cycles
- `GET /farming-cycle/active` - Get active cycle
- `GET /farming-cycle/{cycle_id}/days` - Get farming days
- `GET /farming-cycle/{cycle_id}/stats` - Get statistics

### Feed Management
- `GET /feed/stocks` - List feed stocks
- `POST /feed/stocks/{stock_id}/transaction` - Record transaction
- `GET /feed/stocks/{stock_id}/history` - Get history

### Feeding
- `POST /feed/schedule/{cycle_id}` - Create schedule
- `POST /feed/history/{cycle_id}` - Record feeding
- `GET /feed/history/{cycle_id}` - Get history

### ML Predictions
- `POST /ml/harvest-estimate/{cycle_id}` - Predict harvest date
- `POST /ml/feeding-recommend/{cycle_id}` - Get feeding recommendation
- `GET /ml/models` - List active models
- `GET /ml/models/{id}/performance` - Get model metrics

### Sensors (Existing)
- `GET /sensor-data/latest` - Latest reading
- `POST /sensor-data` - Record data
- `GET /predictions` - AI predictions
- `GET /alerts` - Active alerts
- `GET /notifications` - Notifications

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for detailed documentation.

## 🗄️ Database Schema

### Core Tables
- **users** - User accounts and profiles
- **user_auth** - Email/password credentials
- **farming_cycles** - Farming periods
- **feed_stock** - Feed inventory
- **feed_transactions** - Feed history
- **feeding_schedule** - Scheduled feedings
- **feeding_history** - Actual feeding records
- **harvest_predictions** - ML harvest estimates
- **feeding_recommendations** - ML feeding suggestions
- **sensor_data** - IoT sensor readings
- **predictions** - AI water quality predictions
- **alerts** - Alert records
- **ml_models** - Model metadata

## 🧠 ML Models

### Harvest Estimation
Predicts harvest date based on:
- Days since seeding
- Average water parameters (TDS, pH, DO, temperature)
- Total feed given
- Historical data from similar cycles

**Algorithm**: Random Forest Regression
**Accuracy**: ~85%

### Feeding Optimization
Recommends feeding quantity and timing based on:
- Current farming stage
- Water temperature
- Dissolved oxygen level
- Feed stock availability
- Historical feeding patterns

**Algorithm**: Random Forest Classification + Custom Rules
**Accuracy**: ~80%

## 🔐 Security

- ✅ JWT token-based authentication
- ✅ Bcrypt password hashing
- ✅ SQL injection prevention (parameterized queries)
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ Rate limiting ready
- ✅ Environment variables for secrets

## 📊 Performance

- Connection pooling (10 connections + 20 overflow)
- Query optimization with indexes
- JSONB for complex data
- Response caching headers
- Async-ready architecture
- Horizontal scaling support

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## 📖 Documentation

- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Setup and deployment
- **[API Docs (Interactive)](http://localhost:8000/docs)** - Swagger UI
- **[ReDoc](http://localhost:8000/redoc)** - Alternative API docs

## 🚢 Deployment

### Docker
```bash
docker-compose up --build
```

### Traditional Server
```bash
# Production with gunicorn (4 workers)
gunicorn app.main:app -w 4 -b 0.0.0.0:8000 --timeout 120
```

### Cloud Services
- AWS EC2 / ECS
- Google Cloud Run
- Azure App Service
- Heroku
- DigitalOcean App Platform

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed deployment instructions.

## 🐛 Troubleshooting

### Database Connection Issues
```
Check DATABASE_URL in .env
Verify PostgreSQL is running: pg_isready
```

### Import Errors
```
Install missing dependencies: pip install -r requirements.txt
Run from project root directory
Activate virtual environment
```

### Port Already in Use
```
Use different port: uvicorn app.main:app --port 8001
Or kill process: lsof -ti:8000 | xargs kill -9
```

See [SETUP_GUIDE.md#troubleshooting](./SETUP_GUIDE.md#troubleshooting) for more help.

## 📈 Monitoring & Maintenance

- **Log Monitoring**: Check `app.log` for errors
- **Database Health**: Monitor connections and query performance
- **API Performance**: Track response times and error rates
- **ML Models**: Monitor prediction accuracy over time
- **Sensor Data**: Validate incoming data quality

## 🔄 Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes
# 3. Run tests
pytest tests/ -v

# 4. Commit and push
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature

# 5. Create Pull Request
```

## 📝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- **Robertino Gladden** - Backend Development

## 📞 Support

For issues, questions, or suggestions:
1. Check [FAQ](#faq)
2. Search [existing issues](https://github.com/RobertinoGladden/backend-nila/issues)
3. Create [new issue](https://github.com/RobertinoGladden/backend-nila/issues/new)

## 🙏 Acknowledgments

- FastAPI community
- SQLAlchemy documentation
- scikit-learn & TensorFlow teams
- All contributors and testers

## FAQ

**Q: Can I use SQLite instead of PostgreSQL?**
A: Yes, but PostgreSQL is recommended for production. Change DATABASE_URL in .env.

**Q: Is MQTT required?**
A: No, MQTT is optional. App works without it. Sensor data can be sent via REST API.

**Q: How often should I train the ML models?**
A: Retrain when you have ~100+ new data points or seasonally (every 3 months).

**Q: What's the maximum number of users?**
A: Unlimited with proper infrastructure. Scale database and app servers as needed.

**Q: Can I deploy on Raspberry Pi?**
A: Not recommended for production, but possible for testing. Use ARM-compatible Python version.

---

**Made with ❤️ for aquaculture farmers**
