# ⚡ PANDUAN RINGKAS - QUICK START BAHASA INDONESIA

## 🚀 Start Server (30 Detik)

```bash
cd c:\Users\lapt1\Downloads\Backend NILA
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Buka**: http://localhost:8000/docs ✅

---

## 📊 Semua Endpoint (26 Total)

### 🔐 Auth (5)
```
1. POST   /auth/register              - Daftar
2. POST   /auth/login                 - Login
3. GET    /auth/me                    - Lihat profil
4. PUT    /auth/me                    - Ubah profil
5. POST   /auth/upload-photo          - Upload foto
```

### 🌱 Farming (7)
```
6.  POST   /farming-cycle/            - Buat siklus
7.  GET    /farming-cycle/            - Lihat semua siklus
8.  GET    /farming-cycle/active      - Lihat siklus aktif
9.  GET    /farming-cycle/{id}        - Lihat detail
10. PUT    /farming-cycle/{id}        - Ubah status
11. GET    /farming-cycle/{id}/days   - Hitung hari budidaya
12. GET    /farming-cycle/{id}/stats  - Lihat statistik
```

### 🍖 Feed (8)
```
13. GET    /feed/stocks               - Lihat stok
14. GET    /feed/stocks/{id}          - Lihat stok tertentu
15. POST   /feed/stocks/{id}/transaction - Catat transaksi
16. GET    /feed/stocks/{id}/history  - Lihat riwayat
17. GET    /feed/stocks/{id}/stats    - Lihat statistik
18. POST   /feed/schedule/{id}        - Buat jadwal
19. GET    /feed/schedule/{id}        - Lihat jadwal
20. POST   /feed/history/{id}         - Catat pemberian
21. GET    /feed/history/{id}         - Lihat riwayat pemberian
22. GET    /feed/history/{id}/stats   - Lihat statistik pemberian
```

### 🤖 ML (6)
```
23. POST   /ml/harvest-estimate/{id}  - Prediksi panen
24. GET    /ml/harvest-estimate/{id}  - Lihat prediksi
25. POST   /ml/feeding-recommend/{id} - Rekomendasi pakan
26. GET    /ml/feeding-recommend/{id} - Lihat rekomendasi
27. GET    /ml/models                 - Lihat model AI
28. GET    /ml/models/{id}/performance - Lihat performa
```

---

## 🎯 Skenario Singkat

### Hari 1: Setup
```bash
# 1. Register
POST /auth/register
{
  "email": "petani@gmail.com",
  "password": "Pass123",
  "full_name": "Budi"
}
→ Dapat access_token

# 2. Buat siklus
POST /farming-cycle/
{
  "seeding_date": "2024-01-15"
}
→ Dapat cycle_id = 1

# 3. Beli pakan
POST /feed/stocks/1/transaction
{
  "transaction_type": "input",
  "quantity": 100
}

# 4. Buat jadwal (3x)
POST /feed/schedule/1
{
  "scheduled_time": "07:00",
  "expected_quantity": 5
}
```

### Hari 2-45: Setiap Hari
```bash
# Catat pemberian pagi
POST /feed/history/1
{
  "quantity_given": 5.1,
  "notes": "Pagi"
}

# Catat pemberian siang
POST /feed/history/1
{
  "quantity_given": 5.0,
  "notes": "Siang"
}

# Catat pemberian sore
POST /feed/history/1
{
  "quantity_given": 4.9,
  "notes": "Sore"
}

# Lihat rekomendasi pakan
POST /ml/feeding-recommend/1

# Lihat prediksi panen
POST /ml/harvest-estimate/1
```

### Hari 45: Panen
```bash
# Update status panen
PUT /farming-cycle/1
{
  "status": "completed",
  "actual_harvest_date": "2024-03-25"
}

# Mulai siklus baru
POST /farming-cycle/
{
  "seeding_date": "2024-03-26"
}
```

---

## 🔑 Penting!

✅ **Setiap endpoint perlu token** (dari login)  
✅ **Simpan cycle_id** untuk digunakan di endpoint lain  
✅ **Catat pemberian pakan setiap hari** untuk AI akurat  
✅ **Lihat prediksi & rekomendasi AI** setiap hari  

---

## 📖 Dokumentasi Lengkap

👉 **PANDUAN_LENGKAP_INDONESIA.md** - Full documentation (37KB)

---

**Siap? Buka http://localhost:8000/docs dan mulai! 🚀**
