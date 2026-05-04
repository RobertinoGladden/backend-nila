# 👤 USER MANAGEMENT SYSTEM - API ENDPOINTS REFERENCE

**Version**: 2.0  
**Total New Endpoints**: 10+  
**Language**: 🇮🇩 Indonesian

---

## 📚 DAFTAR ISI

1. [User Profile Management](#profile)
2. [User Dashboard](#dashboard)
3. [Admin User Management](#admin)
4. [Roles & Permissions](#roles)
5. [Complete Example](#example)

---

<a name="profile"></a>

# 👤 USER PROFILE MANAGEMENT (3 Endpoint)

## 📌 ENDPOINT 1: CHANGE PASSWORD - Ubah Password

### Informasi Dasar
```
HTTP Method: PUT
Path: /users/change-password
Query Parameters: old_password, new_password
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (token)
```

### Tujuan
Mengubah password user yang sedang login. Harus verifikasi password lama dulu sebelum bisa ganti.

### Kapan Digunakan?
- ✅ User mau ganti password
- ✅ Password dicuriga sudah diketahui orang lain
- ✅ Halaman "Ubah Password" di aplikasi

### Input

**Header (Wajib)**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
```
old_password=SecurePass123&new_password=NewPass456
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "message": "Password changed successfully"
}
```

**Status 401 (Error - Password Lama Salah)**:
```json
{
  "detail": "Invalid current password"
}
```

**Status 400 (Error - Password Baru Terlalu Pendek)**:
```json
{
  "detail": "New password must be at least 8 characters"
}
```

### Contoh cURL
```bash
curl -X PUT "http://localhost:8000/users/change-password?old_password=SecurePass123&new_password=NewPass456" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Contoh JavaScript
```javascript
const changePassword = async (oldPassword, newPassword) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(
    `http://localhost:8000/users/change-password?old_password=${oldPassword}&new_password=${newPassword}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  const result = await response.json();
  console.log(result.message); // "Password changed successfully"
};

// Usage
await changePassword('SecurePass123', 'NewPass456');
```

### Skenario Penggunaan
```
1. User buka halaman "Ubah Password"
2. User isi password lama & password baru (2x confirm)
3. Klik "Ubah Password"
4. Frontend: PUT /users/change-password?old_password=xxx&new_password=yyy
5. Backend: Verifikasi password lama, ganti dengan baru
6. Response: Sukses
7. Tampilkan: "Password berhasil diubah"
```

### Best Practice
```
✅ LAKUKAN:
  - Verifikasi password lama dengan benar
  - Gunakan password kuat (min 8 char)
  - Show "confirm password" field di form
  - Force user login ulang setelah ganti password

❌ JANGAN:
  - Kirim password di body atau URL yang tidak aman
  - Lupa verifikasi password lama
  - Buat password terlalu lemah
  - Simpan password di plaintext
```

---

## 📌 ENDPOINT 2: DELETE ACCOUNT - Hapus Akun

### Informasi Dasar
```
HTTP Method: DELETE
Path: /users/account
Query Parameters: password
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (token)
```

### Tujuan
Menghapus akun user secara permanent. Harus verifikasi password untuk keamanan.

### Kapan Digunakan?
- ✅ User mau hapus akun mereka
- ✅ User tidak ingin pakai aplikasi lagi
- ✅ Menu "Hapus Akun" di settings

### Input

**Header (Wajib)**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
```
password=SecurePass123
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "message": "Account deleted successfully"
}
```

**Status 401 (Error - Password Salah)**:
```json
{
  "detail": "Invalid password"
}
```

### Contoh cURL
```bash
curl -X DELETE "http://localhost:8000/users/account?password=SecurePass123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Skenario Penggunaan
```
1. User buka Settings → "Hapus Akun"
2. Tampilkan warning: "Akun tidak bisa dipulihkan!"
3. User confirm & input password
4. Frontend: DELETE /users/account?password=xxx
5. Backend: Hapus user & semua data related
6. Response: Sukses
7. Redirect ke halaman public
```

### ⚠️ WARNING
```
PERMANENT ACTION! Semua data akan dihapus:
- User profile
- Farming cycles
- Feed stock
- Predictions
- All related data

Tidak bisa di-undo!
```

---

## 📌 ENDPOINT 3: GET ACCOUNT STATUS - Lihat Status Akun

### Informasi Dasar
```
HTTP Method: GET
Path: /auth/me
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (token)
```

### Output (Status User Included)

**Status 200 (Sukses)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Budi",
  "role": "farmer",
  "status": "active",
  "profile_photo_url": "/uploads/photo.jpg",
  "created_at": "2024-01-15T10:00:00"
}
```

### Status Values
```
"active"   = Akun aktif, bisa pakai
"inactive" = Akun di-pause, hubungi admin
"banned"   = Akun diblokir, hubungi admin support
```

---

<a name="dashboard"></a>

# 📊 USER DASHBOARD (1 Endpoint)

## 📌 ENDPOINT 4: GET USER DASHBOARD - Lihat Dashboard

### Informasi Dasar
```
HTTP Method: GET
Path: /users/dashboard
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (token)
```

### Tujuan
Melihat dashboard personal dengan statistik farming, pakan, dll.

### Kapan Digunakan?
- ✅ Halaman dashboard utama
- ✅ Overview ringkas budidaya user
- ✅ Quick stats untuk quick decision

### Input

**Header (Wajib)**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "user": {
    "id": 1,
    "email": "farmer@example.com",
    "full_name": "Budi Santoso",
    "role": "farmer",
    "status": "active",
    "created_at": "2024-01-15T10:00:00"
  },
  "statistics": {
    "user_id": 1,
    "email": "farmer@example.com",
    "full_name": "Budi Santoso",
    "role": "farmer",
    "status": "active",
    "total_cycles": 5,
    "active_cycles": 2,
    "total_feed_stock": 250.50,
    "created_at": "2024-01-15T10:00:00",
    "last_login": "2024-05-04T17:00:00"
  },
  "message": "Dashboard data retrieved"
}
```

#### Penjelasan Field Output:
| Field | Penjelasan |
|-------|-----------|
| user.id | ID user |
| user.role | Role user (farmer/admin/viewer) |
| user.status | Status akun (active/inactive/banned) |
| statistics.total_cycles | Jumlah siklus budidaya total |
| statistics.active_cycles | Jumlah siklus yang sedang aktif |
| statistics.total_feed_stock | Total pakan tersedia (kg) |
| statistics.last_login | Terakhir login kapan |

### Contoh cURL
```bash
curl -X GET http://localhost:8000/users/dashboard \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Contoh React
```jsx
const Dashboard = () => {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    
    fetch('http://localhost:8000/users/dashboard', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => res.json())
    .then(data => setDashboard(data))
    .catch(err => console.error(err));
  }, []);

  if (!dashboard) return <div>Loading...</div>;

  const { user, statistics } = dashboard;

  return (
    <div className="dashboard">
      <h1>Welcome, {user.full_name}!</h1>
      <p>Role: {user.role}</p>
      
      <div className="stats">
        <div>Total Cycles: {statistics.total_cycles}</div>
        <div>Active: {statistics.active_cycles}</div>
        <div>Feed: {statistics.total_feed_stock} kg</div>
      </div>
    </div>
  );
};
```

### Skenario Penggunaan
```
1. User buka aplikasi
2. Frontend: GET /users/dashboard (kirim token)
3. Backend: Hitung stats user
4. Response: Dashboard data
5. Tampilkan:
   - User info
   - Total cycles: 5
   - Active cycles: 2
   - Total feed: 250.5 kg
   - Last login: 5 hari lalu
```

---

<a name="admin"></a>

# 👨‍💼 ADMIN USER MANAGEMENT (5 Endpoint)

**Catatan**: Semua endpoint admin hanya bisa diakses user dengan role `admin`.

---

## 📌 ENDPOINT 5: LIST ALL USERS - Lihat Semua User

### Informasi Dasar
```
HTTP Method: GET
Path: /users?role=farmer&status=active&skip=0&limit=100
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (admin token)
Query Parameters: role, status, skip, limit (optional)
```

### Tujuan
Melihat daftar semua user di sistem (admin only).

### Input

**Header (Wajib)**:
```
Authorization: Bearer {admin_token}
```

**Query Parameters** (optional):
```
role=farmer       (filter by role: admin/farmer/viewer)
status=active     (filter by status: active/inactive/banned)
skip=0            (offset, default 0)
limit=100         (limit results, default 100)
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
[
  {
    "id": 1,
    "email": "farmer1@example.com",
    "full_name": "Petani Pertama",
    "phone_number": "081234567890",
    "greenhouse_location": "Jakarta",
    "role": "farmer",
    "status": "active",
    "created_at": "2024-01-15T10:00:00"
  },
  {
    "id": 2,
    "email": "farmer2@example.com",
    "full_name": "Petani Kedua",
    "role": "farmer",
    "status": "inactive",
    "created_at": "2024-02-20T14:00:00"
  }
]
```

### Contoh cURL
```bash
# Lihat semua user farmer yang aktif
curl -X GET "http://localhost:8000/users?role=farmer&status=active" \
  -H "Authorization: Bearer {admin_token}"

# Lihat semua user (no filter)
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer {admin_token}"
```

---

## 📌 ENDPOINT 6: GET USER DETAIL - Lihat Detail User

### Informasi Dasar
```
HTTP Method: GET
Path: /users/{id}
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (admin atau user self)
Parameter: id (user ID)
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "id": 1,
  "email": "farmer@example.com",
  "full_name": "Budi Santoso",
  "phone_number": "081234567890",
  "greenhouse_location": "Jakarta",
  "role": "farmer",
  "status": "active",
  "created_at": "2024-01-15T10:00:00"
}
```

---

## 📌 ENDPOINT 7: CHANGE USER ROLE - Ubah Role User

### Informasi Dasar
```
HTTP Method: PUT
Path: /users/{id}/role?role=admin
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (admin token)
Query Parameters: role
```

### Tujuan
Admin mengubah role user (farmer → admin, dll).

### Input

**Query Parameters**:
```
role=admin   (admin/farmer/viewer)
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "id": 1,
  "email": "farmer@example.com",
  "full_name": "Budi",
  "role": "admin",
  "status": "active"
}
```

### Contoh cURL
```bash
# Ubah user 1 jadi admin
curl -X PUT "http://localhost:8000/users/1/role?role=admin" \
  -H "Authorization: Bearer {admin_token}"
```

---

## 📌 ENDPOINT 8: CHANGE USER STATUS - Ubah Status User

### Informasi Dasar
```
HTTP Method: PUT
Path: /users/{id}/status?status=inactive
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (admin token)
Query Parameters: status
```

### Tujuan
Admin mengubah status user (active → inactive → banned).

### Input

**Query Parameters**:
```
status=inactive   (active/inactive/banned)
```

### Status Meanings:
- `active` = User bisa login dan pakai aplikasi
- `inactive` = User di-pause, tidak bisa login
- `banned` = User di-blokir permanen

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "id": 1,
  "email": "farmer@example.com",
  "full_name": "Budi",
  "role": "farmer",
  "status": "inactive"
}
```

### Contoh Skenario
```
Admin melihat user melakukan abuse → change status ke "banned"
User mau break → change status ke "inactive"
User request aktif lagi → change status ke "active"
```

---

## 📌 ENDPOINT 9: DELETE USER - Hapus User

### Informasi Dasar
```
HTTP Method: DELETE
Path: /users/{id}
Status Code: 200 (sukses)
Autentikasi: ✅ DIPERLUKAN (admin token)
Parameter: id (user ID)
```

### Tujuan
Admin menghapus user beserta semua data (permanent).

### Input

**Path Parameter**:
```
{id} = 5 (user ID yang ingin dihapus)
```

### Output (Response Body)

**Status 200 (Sukses)**:
```json
{
  "message": "User deleted successfully"
}
```

**Status 400 (Error - Hapus Diri Sendiri)**:
```json
{
  "detail": "Cannot delete own account"
}
```

### Contoh cURL
```bash
curl -X DELETE http://localhost:8000/users/5 \
  -H "Authorization: Bearer {admin_token}"
```

---

<a name="roles"></a>

# 👥 ROLES & PERMISSIONS MATRIX

## Permission Table

```
FEATURE                     | ADMIN | FARMER | VIEWER
──────────────────────────────────────────────────────
Register                    |  ✅   |   ✅   |  ❌
Login                       |  ✅   |   ✅   |  ✅
GET /auth/me               |  ✅   |   ✅   |  ✅
PUT /auth/me               |  ✅   |   ✅   |  ❌
PUT /users/change-password |  ✅   |   ✅   |  ❌
DELETE /users/account      |  ✅   |   ✅   |  ❌
GET /users/dashboard       |  ✅   |   ✅   |  ✅*
GET /users                 |  ✅   |   ❌   |  ❌
GET /users/{id}            |  ✅   |   ❌** |  ❌
PUT /users/{id}/role       |  ✅   |   ❌   |  ❌
PUT /users/{id}/status     |  ✅   |   ❌   |  ❌
DELETE /users/{id}         |  ✅   |   ❌   |  ❌

* = Dashboard hanya milik sendiri
** = Bisa akses dashboard sendiri, bukan user lain
```

## Role Descriptions

### ADMIN (Administrator)
- ✅ Full system access
- ✅ Manage all users
- ✅ Change user roles & status
- ✅ Delete users
- ✅ Access to admin endpoints

### FARMER (Petani/Regular User)
- ✅ Register & login
- ✅ Manage own farm data
- ✅ View own dashboard
- ✅ Change own password
- ✅ Delete own account
- ❌ Access other users' data
- ❌ Admin functions

### VIEWER (Pembaca/Read-Only)
- ✅ Login
- ✅ View own profile
- ✅ View shared data
- ❌ Modify any data
- ❌ Manage farm data
- ❌ Admin functions

---

<a name="example"></a>

# 📝 COMPLETE EXAMPLE - Admin Flow

## Scenario: Admin membuat akun farmer baru

```
1. Admin login
   POST /auth/login
   { email: "admin@example.com", password: "AdminPass123" }
   ✓ Get token A

2. Admin lihat semua user farmers
   GET /users?role=farmer&status=active
   Header: Authorization: Bearer TokenA
   ✓ Get list of farmers

3. Admin lihat detail satu farmer
   GET /users/5
   Header: Authorization: Bearer TokenA
   ✓ Get farmer details

4. Farmer melakukan abuse, admin ban
   PUT /users/5/status?status=banned
   Header: Authorization: Bearer TokenA
   ✓ User 5 sudah di-ban

5. Farmer komplain, admin unban
   PUT /users/5/status?status=active
   Header: Authorization: Bearer TokenA
   ✓ User 5 sudah aktif lagi

6. User minta jadi admin, admin promote
   PUT /users/5/role?role=admin
   Header: Authorization: Bearer TokenA
   ✓ User 5 sekarang admin

7. Admin delete user yang tidak perlu
   DELETE /users/10
   Header: Authorization: Bearer TokenA
   ✓ User 10 dihapus
```

---

## ✅ SUMMARY - 10 New Endpoints

✅ **User Profile (3 endpoint)**
- PUT /users/change-password
- DELETE /users/account
- GET /auth/me (updated with role/status)

✅ **User Dashboard (1 endpoint)**
- GET /users/dashboard

✅ **Admin Management (5 endpoint)**
- GET /users
- GET /users/{id}
- PUT /users/{id}/role
- PUT /users/{id}/status
- DELETE /users/{id}

✅ **Plus existing auth endpoints (5)**
- POST /auth/register
- POST /auth/login
- PUT /auth/me
- POST /auth/upload-photo

**Total: 26+ Endpoints** 🚀

---

**System ready for production! Deploy now!** 🎉
