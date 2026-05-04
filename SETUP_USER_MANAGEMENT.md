# 🚀 USER MANAGEMENT SYSTEM - SETUP & TESTING GUIDE

**Language**: 🇮🇩 Indonesian  
**Status**: ✅ Ready to Deploy

---

## 📋 QUICK START (3 Steps)

### STEP 1: Restart Backend dengan Database Schema Baru

```bash
# 1. Tekan CTRL+C di terminal uvicorn (stop server lama)

# 2. Jalankan database initialization
cd "c:\Users\lapt1\Downloads\Backend NILA"
python init_app_db.py

# Output expected:
# 🔄 Creating all database tables...
# ✅ Database tables created successfully!
# 🔄 Applying User Management Schema...
# ✅ User Management Schema applied!
# 📋 Created tables (17 total):
#    - users
#    - ... dll

# 3. Jalankan backend baru
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Output expected:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

### STEP 2: Register User Pertama (untuk testing)

```bash
# Buka terminal baru, jalankan:
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"farmer1@example.com\",
    \"password\": \"SecurePass123\",
    \"full_name\": \"Petani Budi\",
    \"phone_number\": \"081234567890\",
    \"greenhouse_location\": \"Jakarta\",
    \"address\": \"Jl. Merdeka No. 1\"
  }"

# Expected response:
# {
#   "id": 1,
#   "email": "farmer1@example.com",
#   "full_name": "Petani Budi",
#   "role": "farmer",        ← Auto-set!
#   "status": "active",       ← Auto-set!
#   "message": "User registered successfully"
# }
```

### STEP 3: Login & Test Dashboard

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"farmer1@example.com\", \"password\": \"SecurePass123\"}"

# Expected response (save TOKEN):
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "user": {
#     "id": 1,
#     "email": "farmer1@example.com",
#     "role": "farmer",
#     "status": "active"
#   }
# }

# Test dashboard (ganti TOKEN dengan dari response di atas)
curl -X GET http://localhost:8000/users/dashboard \
  -H "Authorization: Bearer TOKEN"

# Expected response:
# {
#   "user": { ... },
#   "statistics": {
#     "total_cycles": 0,
#     "active_cycles": 0,
#     "total_feed_stock": 0
#   }
# }
```

---

## 🧪 FULL TEST SUITE

Jalankan setiap curl command di terminal, verifikasi response-nya.

### A. AUTHENTICATION & PROFILE

#### Test 1: Register Multiple Users
```bash
# User 2 (untuk admin testing nanti)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"admin@example.com\",
    \"password\": \"AdminPass123\",
    \"full_name\": \"Admin System\",
    \"phone_number\": \"089999999999\",
    \"greenhouse_location\": \"Bandung\",
    \"address\": \"Jl. Admin No. 5\"
  }"

# User 3 (untuk viewer testing)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"viewer@example.com\",
    \"password\": \"ViewerPass123\",
    \"full_name\": \"Pemilik Viewer\",
    \"phone_number\": \"087777777777\",
    \"greenhouse_location\": \"Surabaya\",
    \"address\": \"Jl. View No. 3\"
  }"

# Verify: 3 users created dengan role "farmer" default
```

#### Test 2: Login All Users
```bash
# Login farmer
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"farmer1@example.com\", \"password\": \"SecurePass123\"}"
# Save token → $TOKEN_FARMER

# Login admin
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@example.com\", \"password\": \"AdminPass123\"}"
# Save token → $TOKEN_ADMIN

# Login viewer
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"viewer@example.com\", \"password\": \"ViewerPass123\"}"
# Save token → $TOKEN_VIEWER

# Verify: last_login timestamp updated di database
# Check command di PowerShell:
# (Get-Content session_state.txt) | Select-String "last_login"
```

#### Test 3: Get Account Status
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN_FARMER"

# Expected: role="farmer", status="active"
```

---

### B. USER DASHBOARD

#### Test 4: View Dashboard
```bash
curl -X GET http://localhost:8000/users/dashboard \
  -H "Authorization: Bearer $TOKEN_FARMER"

# Expected: total_cycles=0, active_cycles=0, total_feed_stock=0
```

---

### C. USER PROFILE MANAGEMENT

#### Test 5: Change Password
```bash
# Change farmer password
curl -X PUT "http://localhost:8000/users/change-password?old_password=SecurePass123&new_password=NewSecure456" \
  -H "Authorization: Bearer $TOKEN_FARMER"

# Expected: {"message": "Password changed successfully"}

# Verify: Login dengan password baru berfungsi
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"farmer1@example.com\", \"password\": \"NewSecure456\"}"
# Expected: Login sukses dengan token baru
```

#### Test 6: Delete Account
```bash
# Create temporary user untuk di-delete
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"temp@example.com\",
    \"password\": \"TempPass123\",
    \"full_name\": \"Temporary User\",
    \"phone_number\": \"081111111111\",
    \"greenhouse_location\": \"Jakarta\",
    \"address\": \"Jl. Temp No. 1\"
  }"

# Get token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"temp@example.com\", \"password\": \"TempPass123\"}"
# Save token → $TOKEN_TEMP

# Delete account
curl -X DELETE "http://localhost:8000/users/account?password=TempPass123" \
  -H "Authorization: Bearer $TOKEN_TEMP"

# Expected: {"message": "Account deleted successfully"}

# Verify: Login dengan email temp tidak bisa
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"temp@example.com\", \"password\": \"TempPass123\"}"
# Expected: Error atau tidak ada user
```

---

### D. ADMIN FUNCTIONS (Promote Admin First)

#### Step: Promote Admin
```bash
# Manual SQL to promote user 2 to admin:
# di pgAdmin4 atau psql:
# UPDATE users SET role = 'admin' WHERE id = 2;

# OR via manual endpoint (jika sudah ada super-admin setup)
# Untuk testing sekarang, lakukan manual promotion di database

# Verify via API:
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN_ADMIN"
# Expected: role="admin"
```

#### Test 7: List All Users (Admin Only)
```bash
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Expected: Array dengan 3 users
# [
#   { id: 1, email: "farmer1@example.com", role: "farmer", status: "active" },
#   { id: 2, email: "admin@example.com", role: "admin", status: "active" },
#   { id: 3, email: "viewer@example.com", role: "viewer", status: "active" }
# ]
```

#### Test 8: Get User Detail (Admin)
```bash
curl -X GET http://localhost:8000/users/1 \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Expected: User 1 full detail
```

#### Test 9: Change User Role
```bash
# Promote viewer jadi farmer
curl -X PUT "http://localhost:8000/users/3/role?role=farmer" \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Expected: User 3 role updated to "farmer"

# Verify
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN_VIEWER"
# Expected: role="farmer" sekarang
```

#### Test 10: Change User Status
```bash
# Ban farmer
curl -X PUT "http://localhost:8000/users/1/status?status=banned" \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Expected: User 1 status updated to "banned"

# Verify: Farmer tidak bisa login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"farmer1@example.com\", \"password\": \"NewSecure456\"}"
# Expected: Error "Account is inactive"

# Unban farmer
curl -X PUT "http://localhost:8000/users/1/status?status=active" \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Verify: Farmer bisa login lagi
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"farmer1@example.com\", \"password\": \"NewSecure456\"}"
# Expected: Login sukses
```

#### Test 11: Delete User (Admin)
```bash
# Create another temporary user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"delete_me@example.com\",
    \"password\": \"DeletePass123\",
    \"full_name\": \"Delete Me User\",
    \"phone_number\": \"081111111112\",
    \"greenhouse_location\": \"Jakarta\",
    \"address\": \"Jl. Delete No. 1\"
  }"

# Get user ID (should be 5 or 6)
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer $TOKEN_ADMIN"
# Find delete_me@example.com → id

# Delete as admin
curl -X DELETE "http://localhost:8000/users/5" \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Expected: {"message": "User deleted successfully"}

# Verify: User tidak di database
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer $TOKEN_ADMIN"
# Expected: delete_me@example.com tidak ada
```

---

### E. PERMISSION TESTS

#### Test 12: Farmer Cannot Access Admin Endpoints
```bash
# Try list all users as farmer
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer $TOKEN_FARMER"

# Expected: Error 403 Forbidden atau similar
# {"detail": "Not authorized"}
```

#### Test 13: Viewer Cannot Change Password
```bash
# Change password as viewer
curl -X PUT "http://localhost:8000/users/change-password?old_password=ViewerPass123&new_password=NewViewer456" \
  -H "Authorization: Bearer $TOKEN_VIEWER"

# Expected: Error 403 Forbidden
```

---

## 📊 DATABASE VERIFICATION

### Check if tables updated correctly:

**Via psql/pgAdmin4**:
```sql
-- Check users table columns
\d users
-- Should see: role, status, last_login, is_email_verified

-- Check user data
SELECT id, email, role, status, last_login FROM users;
-- Should see all users dengan role & status populated

-- Check indexes
\d+ users
-- Should see: idx_user_role, idx_user_status, idx_user_email_verified
```

**Via Python**:
```python
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
users = db.query(User).all()
for user in users:
    print(f"{user.email} | role={user.role} | status={user.status} | last_login={user.last_login}")
db.close()
```

---

## ✅ TESTING CHECKLIST

### Registration & Login
- [ ] User dapat register
- [ ] Default role = "farmer"
- [ ] Default status = "active"
- [ ] User dapat login
- [ ] last_login timestamp ter-set

### User Profile
- [ ] GET /auth/me menampilkan role & status
- [ ] PUT /change-password berfungsi
- [ ] DELETE /account menghapus user

### Dashboard
- [ ] GET /dashboard menampilkan stats
- [ ] Stats ter-calculate dengan benar

### Admin Features
- [ ] GET /users menampilkan semua user
- [ ] GET /users/{id} menampilkan detail
- [ ] PUT /users/{id}/role mengubah role
- [ ] PUT /users/{id}/status mengubah status
- [ ] DELETE /users/{id} menghapus user

### Permissions
- [ ] Farmer tidak bisa akses admin endpoints
- [ ] Viewer tidak bisa modify data
- [ ] Only admin bisa manage users
- [ ] Banned users tidak bisa login
- [ ] Inactive users tidak bisa login

---

## 🐛 TROUBLESHOOTING

### Error: "ModuleNotFoundError: No module named..."
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or specific packages
pip install fastapi uvicorn pydantic sqlalchemy psycopg2-binary
```

### Error: "Could not connect to database"
```bash
# Check PostgreSQL running
# Windows: Services → PostgreSQL
# Or via command:
psql -U postgres -d postgres -c "SELECT 1"

# Check connection string di app/database.py
# Default: postgresql://user:password@localhost:5432/nila_db
```

### Error: "password cannot be longer than 72 bytes"
```bash
# Already fixed in schemas.py
# Password automatically truncated to 72 bytes
# Try dengan password lebih pendek untuk testing
```

### Database tables tidak ada setelah init
```bash
# Run init_app_db.py again
python init_app_db.py

# Check error messages di output
# Mungkin ada permission issue atau connection problem
```

### Admin cannot access endpoints
```bash
# Check role di database
SELECT id, email, role FROM users WHERE email = 'admin@example.com';

# If role not 'admin', update manually:
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

---

## 🚀 PRODUCTION CHECKLIST

Before deploying to production:

- [ ] Database migration run successfully
- [ ] All tests passing (see checklist above)
- [ ] Change PostgreSQL password (not default)
- [ ] Set JWT secret key di environment variable
- [ ] Enable HTTPS in production
- [ ] Set CORS origins properly
- [ ] Add rate limiting for auth endpoints
- [ ] Setup email verification (optional)
- [ ] Setup monitoring/logging
- [ ] Backup database regularly

---

## 📞 SUPPORT

Jika ada error atau pertanyaan, check:

1. **Backend Logs** - cek terminal uvicorn
2. **Database Logs** - cek PostgreSQL
3. **API Documentation** - http://localhost:8000/docs
4. **Endpoints Guide** - USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md

**Happy farming! 🌾🐟**
