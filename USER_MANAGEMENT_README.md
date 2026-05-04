# 👥 USER MANAGEMENT SYSTEM v2.0

**Backend NILA - Complete User & Admin Management**

🎉 **Production Ready** | 🇮🇩 Indonesian Support | 📊 10+ New Endpoints | 🔐 Role-Based Access Control

---

## 📋 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [What's Included](#whats-included)
3. [Features Overview](#features-overview)
4. [Installation & Setup](#installation--setup)
5. [API Endpoints](#api-endpoints)
6. [Documentation Files](#documentation-files)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 QUICK START

### 3 Steps to Get Running

```bash
# Step 1: Initialize Database
cd "c:\Users\lapt1\Downloads\Backend NILA"
python init_app_db.py

# Step 2: Start Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Step 3: Test It (in new terminal)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"SecurePass123\",\"full_name\":\"Test User\",\"phone_number\":\"081234567890\",\"greenhouse_location\":\"Jakarta\",\"address\":\"Jl Test\"}"
```

**Expected Response** (Save the token!):
```json
{
  "id": 1,
  "email": "test@example.com",
  "full_name": "Test User",
  "role": "farmer",        ← Auto-set
  "status": "active",      ← Auto-set
  "message": "User registered successfully"
}
```

---

## ✅ WHAT'S INCLUDED

### 📦 Implementation

- ✅ **User Authentication** - Register, login, JWT tokens
- ✅ **Profile Management** - Change password, delete account
- ✅ **Dashboard** - Personal statistics & overview
- ✅ **Admin Panel** - 5 endpoints to manage all users
- ✅ **Role-Based Access** - Admin, Farmer, Viewer roles
- ✅ **Status System** - Active, Inactive, Banned status
- ✅ **Security** - Password hashing, bcrypt, validation
- ✅ **Audit Trail** - Last login tracking

### 📄 Documentation

- ✅ **USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md** (16KB)
  - Complete API reference for all 10+ endpoints
  - cURL examples, JavaScript/React code
  - Request/response examples

- ✅ **SETUP_USER_MANAGEMENT.md** (14KB)
  - Step-by-step setup guide
  - 13 comprehensive test cases
  - Database verification
  - Troubleshooting guide

- ✅ **QUICK_REFERENCE_USER_MANAGEMENT.md** (4KB)
  - Quick command reference
  - Common workflows
  - Bookmarkable cheat sheet

- ✅ **test_user_management.bat** (Windows batch script)
  - Auto-test script for quick validation
  - Guides through registration & login flow

### 💻 Code Files

- ✅ **app/services/user_service.py** - User management logic
- ✅ **app/routers/users.py** - User API endpoints
- ✅ **app/models.py** - Updated User model with role/status
- ✅ **app/schemas.py** - Updated schemas with validation
- ✅ **app/services/auth_service.py** - Enhanced auth with status check
- ✅ **init_app_db.py** - Auto-migration script

---

## 🎯 FEATURES OVERVIEW

### User Registration
```json
POST /auth/register
{
  "email": "farmer@example.com",
  "password": "SecurePass123",
  "full_name": "Budi Santoso",
  "phone_number": "081234567890",
  "greenhouse_location": "Jakarta",
  "address": "Jl. Merdeka No. 1"
}

RESPONSE:
{
  "id": 1,
  "role": "farmer",        ← Automatic!
  "status": "active"       ← Automatic!
}
```

### User Login
```json
POST /auth/login
{
  "email": "farmer@example.com",
  "password": "SecurePass123"
}

RESPONSE:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": { "id": 1, "role": "farmer", "status": "active" }
}
```

### User Dashboard
```json
GET /users/dashboard
Header: Authorization: Bearer {token}

RESPONSE:
{
  "user": { "email": "farmer@example.com", "role": "farmer" },
  "statistics": {
    "total_cycles": 5,
    "active_cycles": 2,
    "total_feed_stock": 250.50,
    "last_login": "2024-05-04T17:00:00"
  }
}
```

### Admin User Management
```json
GET /users                    ← List all users
GET /users/{id}               ← View user detail
PUT /users/{id}/role          ← Change role
PUT /users/{id}/status        ← Ban/inactive user
DELETE /users/{id}            ← Delete user

Header: Authorization: Bearer {admin_token}
```

---

## 🔧 INSTALLATION & SETUP

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
cd "c:\Users\lapt1\Downloads\Backend NILA"
pip install -r requirements.txt

# Verify key packages:
pip list | grep -E "fastapi|sqlalchemy|psycopg2|pydantic"
```

### Step 2: Database Setup
```bash
# Initialize database with new schema
python init_app_db.py

# Expected output:
# ✅ Database tables created successfully!
# ✅ User Management Schema applied!
# 📋 Created tables (17 total):
#    - users (with new columns!)
#    - user_auth
#    - farming_cycles
#    - ... (14 more)
```

### Step 3: Verify Database Changes
```bash
# In pgAdmin4 or psql:
SELECT id, email, role, status, last_login FROM users LIMIT 5;

# Should see columns:
# - role (VARCHAR 'farmer'|'admin'|'viewer')
# - status (VARCHAR 'active'|'inactive'|'banned')
# - last_login (TIMESTAMP)
# - is_email_verified (BOOLEAN)
```

### Step 4: Start Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

### Step 5: Verify via API Docs
- Open browser: http://localhost:8000/docs
- See all 26+ endpoints including new user management endpoints
- Try-it-out functionality available

---

## 🌐 API ENDPOINTS

### Authentication (5 endpoints)
```
POST   /auth/register                    - Register new user
POST   /auth/login                       - Login & get JWT token
GET    /auth/me                          - Get current user (with role/status)
PUT    /auth/me                          - Update profile
POST   /auth/upload-photo                - Upload profile picture
```

### User Profile (3 endpoints) ⭐ NEW
```
PUT    /users/change-password            - Change password
DELETE /users/account                    - Delete own account
GET    /users/dashboard                  - View personal dashboard
```

### Admin Management (5 endpoints) ⭐ NEW
```
GET    /users                            - List all users
GET    /users/{id}                       - Get user detail
PUT    /users/{id}/role                  - Change user role
PUT    /users/{id}/status                - Change user status
DELETE /users/{id}                       - Delete user
```

**Admin endpoints require `role='admin'` and valid JWT token**

---

## 📚 DOCUMENTATION FILES

### Main Documentation

| File | Size | Content |
|------|------|---------|
| **USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md** | 16KB | Complete API reference with examples |
| **SETUP_USER_MANAGEMENT.md** | 14KB | Setup, testing, troubleshooting |
| **QUICK_REFERENCE_USER_MANAGEMENT.md** | 4KB | Quick command reference (bookmark!) |
| **USER_MANAGEMENT_IMPLEMENTATION_COMPLETE.md** | 13KB | Technical implementation details |
| **test_user_management.bat** | 2.7KB | Automated test script for Windows |

### In-Code Documentation

- **app/services/user_service.py** - Docstrings for all functions
- **app/routers/users.py** - Endpoint documentation
- **app/models.py** - Model field descriptions

---

## 🔐 SECURITY FEATURES

### Authentication
- ✅ JWT tokens (stateless, scalable)
- ✅ Bcrypt password hashing (industry standard)
- ✅ Password strength validation (minimum 8 characters)
- ✅ Password size limit (72 bytes - bcrypt requirement)

### Authorization
- ✅ Role-based access control (RBAC)
  - **Admin**: Full system access
  - **Farmer**: Own data only
  - **Viewer**: Read-only access

- ✅ Status-based access blocking
  - **active**: Can login and use app
  - **inactive**: Cannot login (soft disable)
  - **banned**: Permanently blocked

### Data Protection
- ✅ Cascade delete (delete user → delete related data)
- ✅ Audit trail (last_login timestamp)
- ✅ Token validation on every protected request

---

## 👥 ROLES & PERMISSIONS

### Permission Matrix

```
FEATURE                     | ADMIN | FARMER | VIEWER
────────────────────────────────────────────────────────
Register & Login            |  ✅   |   ✅   |   ✅
View own profile            |  ✅   |   ✅   |   ✅
Change own password         |  ✅   |   ✅   |   ❌
Delete own account          |  ✅   |   ✅   |   ❌
View own dashboard          |  ✅   |   ✅   |   ✅*
Manage own data (farm, feed)|  ✅   |   ✅   |   ❌
────────────────────────────────────────────────────────
List all users              |  ✅   |   ❌   |   ❌
View any user detail        |  ✅   |   ❌   |   ❌
Change user role            |  ✅   |   ❌   |   ❌
Change user status (ban)    |  ✅   |   ❌   |   ❌
Delete any user             |  ✅   |   ❌   |   ❌

* = Dashboard shows own data only
```

---

## 🧪 TESTING

### Quick Test (2 minutes)
```bash
# Run automated test script (Windows only)
test_user_management.bat

# Follow on-screen instructions
```

### Manual Testing (cURL)
```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass123456","full_name":"Test"}'

# 2. Login (save token)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass123456"}'

# 3. View dashboard
curl -X GET http://localhost:8000/users/dashboard \
  -H "Authorization: Bearer eyJhbGc..."
```

### Full Test Suite
See **SETUP_USER_MANAGEMENT.md** for 13 comprehensive test cases covering:
- Registration & login flow
- Profile management (change password, delete account)
- Dashboard functionality
- Admin features (list, edit, delete users)
- Permission enforcement
- Status & role changes

---

## 🆘 TROUBLESHOOTING

### Q1: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt

# Or specific packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
```

### Q2: "Could not connect to database"
```bash
# Check PostgreSQL is running
# Windows Services → PostgreSQL should be "Running"

# Or verify connection
psql -U postgres -d postgres -c "SELECT 1"

# Check connection string in app/database.py
# Default: postgresql://user:password@localhost:5432/nila_db
```

### Q3: "password cannot be longer than 72 bytes"
```bash
# This is fixed in the new code
# But if you still see it, use shorter password for testing
# Max: 72 bytes in UTF-8
```

### Q4: "Not authorized" (403 error)
```bash
# Check 1: You have valid JWT token?
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Check 2: Trying admin endpoint as non-admin?
# Promote user to admin first (manual or via SQL)
UPDATE users SET role='admin' WHERE email='admin@example.com';

# Check 3: User is banned?
# Check user status
SELECT email, status FROM users WHERE email='admin@example.com';
```

### Q5: User can't login
```bash
# Reason 1: Status is not 'active'
SELECT email, status FROM users;
UPDATE users SET status='active' WHERE email='user@example.com';

# Reason 2: Wrong password
# Password is case-sensitive and space-sensitive

# Reason 3: User not in database
SELECT * FROM users WHERE email='user@example.com';
```

**For more help**, see **SETUP_USER_MANAGEMENT.md** Troubleshooting section.

---

## 📊 DATABASE SCHEMA CHANGES

### Columns Added to `users` Table

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'farmer';
ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN DEFAULT FALSE;
```

### New Indexes Created

```sql
CREATE INDEX idx_user_role ON users(role);
CREATE INDEX idx_user_status ON users(status);
CREATE INDEX idx_user_email_verified ON users(is_email_verified);
```

Automatically applied by `init_app_db.py` on first run.

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] Run `python init_app_db.py` (database setup)
- [ ] Verify all tables created: `\dt` in psql
- [ ] Check new columns exist: `\d users` in psql
- [ ] Restart backend: `CTRL+C` then `uvicorn app.main:app`
- [ ] Test registration: `curl -X POST http://localhost:8000/auth/register ...`
- [ ] Test login: `curl -X POST http://localhost:8000/auth/login ...`
- [ ] Test dashboard: `curl -X GET http://localhost:8000/users/dashboard ...`

### Testing
- [ ] Run all 13 tests from **SETUP_USER_MANAGEMENT.md**
- [ ] Test with different user roles (admin, farmer, viewer)
- [ ] Verify permission enforcement
- [ ] Check database for audit trail (last_login)

### Production
- [ ] Change PostgreSQL default password
- [ ] Set JWT secret key (environment variable)
- [ ] Enable HTTPS
- [ ] Setup backup strategy
- [ ] Setup monitoring/logging
- [ ] Create initial admin account

---

## 📞 SUPPORT & HELP

### Documentation Order (Read in this order)
1. **This file** - Overview & quick start
2. **QUICK_REFERENCE_USER_MANAGEMENT.md** - Copy-paste commands
3. **USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md** - Full API reference
4. **SETUP_USER_MANAGEMENT.md** - Detailed testing & troubleshooting

### Finding Information
- **"How do I...?"** → Check QUICK_REFERENCE_USER_MANAGEMENT.md
- **"What endpoints exist?"** → USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md
- **"How do I test?"** → SETUP_USER_MANAGEMENT.md or test_user_management.bat
- **"What changed?"** → USER_MANAGEMENT_IMPLEMENTATION_COMPLETE.md

---

## 📈 NEXT STEPS

### Immediate (Next Sprint)
- [ ] Run all tests from this guide
- [ ] Promote first admin via database
- [ ] Test admin endpoints
- [ ] Integrate into frontend

### Phase 2 (Future Enhancement)
- [ ] Email verification workflow
- [ ] Password reset via email
- [ ] Two-factor authentication (2FA)
- [ ] OAuth integration (Google, Facebook)
- [ ] User activity audit log
- [ ] Bulk user import/export
- [ ] Team/group management

---

## 📝 NOTES

### Version History
- **v2.0** - Complete user management system with RBAC (current)
- **v1.0** - Basic authentication only

### Backward Compatibility
✅ All existing endpoints still work
✅ New fields have sensible defaults
✅ No breaking changes

### Performance
- Database indexes on role, status, email_verified for fast queries
- JWT tokens stateless (scalable)
- No N+1 query problems

---

## 🎉 YOU'RE READY!

Everything is set up and documented. Choose your next step:

- **Quick Test**: Run `test_user_management.bat`
- **Detailed Setup**: Follow SETUP_USER_MANAGEMENT.md
- **API Reference**: Read USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md
- **Integration**: Copy examples from QUICK_REFERENCE_USER_MANAGEMENT.md

---

**Happy farming! 🌾🐟**

Questions? Errors? See troubleshooting section or check the detailed documentation files.
