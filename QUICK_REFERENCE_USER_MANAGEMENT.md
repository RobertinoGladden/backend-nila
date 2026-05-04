# 🚀 USER MANAGEMENT - QUICK REFERENCE

**Bookmark this!** ⭐

---

## 🔐 AUTHENTICATION

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123456","full_name":"Name"}'

# Login (save token!)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123456"}'

# Get current user
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## 👤 USER PROFILE

```bash
# View dashboard
curl -X GET http://localhost:8000/users/dashboard \
  -H "Authorization: Bearer $TOKEN"

# Change password
curl -X PUT "http://localhost:8000/users/change-password?old_password=OLD&new_password=NEW" \
  -H "Authorization: Bearer $TOKEN"

# Delete account
curl -X DELETE "http://localhost:8000/users/account?password=PASS" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 👨‍💼 ADMIN ONLY

```bash
# List all users
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Get user detail
curl -X GET http://localhost:8000/users/1 \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Change user role (admin/farmer/viewer)
curl -X PUT "http://localhost:8000/users/1/role?role=admin" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Change user status (active/inactive/banned)
curl -X PUT "http://localhost:8000/users/1/status?status=banned" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Delete user
curl -X DELETE http://localhost:8000/users/1 \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## 🔑 VARIABLES

```bash
# Set token after login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
ADMIN_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Use in curl
curl ... -H "Authorization: Bearer $TOKEN"
```

---

## 📊 STATUS & ROLES

| Status | Meaning |
|--------|---------|
| `active` | Can login & use app |
| `inactive` | Cannot login |
| `banned` | Blocked permanently |

| Role | Permissions |
|------|-------------|
| `admin` | Full system access |
| `farmer` | Own data only |
| `viewer` | Read-only |

---

## 🔄 COMMON WORKFLOWS

### Admin Promote User to Admin
```bash
curl -X PUT "http://localhost:8000/users/2/role?role=admin" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Admin Ban User
```bash
curl -X PUT "http://localhost:8000/users/3/status?status=banned" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### User Change Password
```bash
curl -X PUT "http://localhost:8000/users/change-password?old_password=OLD123&new_password=NEW123" \
  -H "Authorization: Bearer $TOKEN"
```

### Admin Delete User
```bash
curl -X DELETE http://localhost:8000/users/5 \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## 🧪 QUICK TEST

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456","full_name":"Test"}'

# 2. Login (copy token)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'

# 3. View dashboard
curl -X GET http://localhost:8000/users/dashboard \
  -H "Authorization: Bearer TOKEN_HERE"
```

---

## 📖 FULL DOCS

- **Complete API**: `USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md`
- **Setup & Testing**: `SETUP_USER_MANAGEMENT.md`
- **Full Details**: `USER_MANAGEMENT_IMPLEMENTATION_COMPLETE.md`

---

**Quick tip**: Use PowerShell to make $TOKEN variables reusable!

```powershell
$TOKEN = "eyJhbGciOi..."
curl -X GET http://localhost:8000/auth/me -H "Authorization: Bearer $TOKEN"
```

---

🎉 **You're ready!** Start building!
