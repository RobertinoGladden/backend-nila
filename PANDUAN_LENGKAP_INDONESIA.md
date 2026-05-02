# 📖 PANDUAN LENGKAP BACKEND NILA - BAHASA INDONESIA

**Versi**: 1.0  
**Tanggal**: Januari 2024  
**Status**: Lengkap & Siap Pakai  
**Bahasa**: 🇮🇩 Bahasa Indonesia

---

## 📚 DAFTAR ISI

1. [Pengenalan Backend NILA](#pengenalan)
2. [Cara Menjalankan](#cara-menjalankan)
3. [Semua Endpoint Dijelaskan](#semua-endpoint)
4. [Contoh Penggunaan Real](#contoh-real)
5. [Tips & Trik](#tips)
6. [Troubleshooting](#troubleshooting)

---

<a name="pengenalan"></a>

# 🎯 BAGIAN 1: PENGENALAN BACKEND NILA

## Apa Itu Backend NILA?

**Backend NILA** adalah sistem komputer di balik layar untuk mengelola budidaya ikan/udang.

### Analogi Sederhana:

Bayangkan Anda punya **toko kelontong**:
- **Pelanggan** = Aplikasi mobile (Flutter/React)
- **Kasir** = Backend NILA
- **Gudang** = Database PostgreSQL
- **Barang dagangan** = Data (user, farming, pakan, dll)

Pelanggan datang ke kasir untuk:
- ✅ Daftar akun
- ✅ Cek stok pakan
- ✅ Lihat prediksi panen
- ✅ Catat pemberian pakan

Kasir (Backend) mengelola semua itu dengan meminta/menyimpan data ke gudang (Database).

## Teknologi yang Digunakan

| Komponen | Teknologi | Kegunaan |
|----------|-----------|---------|
| **Framework** | FastAPI | Web server Python modern |
| **Database** | PostgreSQL | Menyimpan semua data (users, farming, pakan, dll) |
| **Autentikasi** | JWT + Bcrypt | Keamanan login & password |
| **AI/ML** | scikit-learn | Prediksi panen & rekomendasi pakan |
| **Real-time** | MQTT | Sensor data real-time |

## Apa yang Bisa Dilakukan?

✅ **User Management**
- Daftar akun baru
- Login aman
- Ubah profil
- Upload foto

✅ **Farming Management**
- Buat siklus budidaya baru
- Tracking dari penebaran sampai panen
- Hitung berapa hari budidaya
- Lihat statistik

✅ **Feed Management**
- Catat beli pakan
- Catat pemberian pakan
- Lihat riwayat pakan
- Cek stok pakan

✅ **AI/ML Predictions**
- Prediksi kapan waktu panen
- Rekomendasi berapa banyak pakan yang harus diberikan
- Akurasi AI terus meningkat

✅ **Sensor Integration**
- Terima data sensor real-time (TDS, pH, DO, Suhu)
- Kalibrasi sensor otomatis
- Alert jika ada masalah air

---

<a name="cara-menjalankan"></a>

# 🚀 BAGIAN 2: CARA MENJALANKAN BACKEND

## Langkah 1: Persiapan (Hanya Sekali)

### Buka Command Prompt

Tekan `Win + R`, ketik `cmd`, tekan Enter

### Navigasi ke Folder Project

```bash
cd c:\Users\lapt1\Downloads\Backend NILA
```

### Buat Virtual Environment (Ruang Terisolasi untuk Python)

```bash
python -m venv venv
```

**Apa itu?** Membuat folder `venv` yang berisi semua library project Anda terpisah dari sistem.

### Aktifkan Virtual Environment

```bash
venv\Scripts\activate
```

**Hasil**: Prompt akan berubah menjadi:
```
(venv) c:\Users\lapt1\Downloads\Backend NILA>
```

### Install Semua Library yang Dibutuhkan

```bash
pip install -r requirements.txt
```

**Apa yang terjadi?**
- Download FastAPI, PostgreSQL driver, ML libraries, dll
- Waktu: 2-5 menit
- Tunggu sampai selesai

### Setup Database (Hanya Kali Pertama)

```bash
python init_app_db.py
```

**Output sukses**:
```
🔄 Creating all database tables...
✅ Database tables created successfully!

📋 Created tables (17 total):
   - users
   - farming_cycles
   - feed_stock
   - ... (dan lainnya)

✨ Database initialization complete!
```

## Langkah 2: Jalankan Server (Setiap Kali Ingin Pakai)

### Aktifkan Virtual Environment Lagi

```bash
cd c:\Users\lapt1\Downloads\Backend NILA
venv\Scripts\activate
```

### Jalankan Server

```bash
uvicorn app.main:app --reload
```

**Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Akses API

Buka browser dan buka: **http://localhost:8000/docs**

**Anda akan melihat**: Interface Swagger UI dengan semua endpoint terdaftar

## Langkah 3: Berhenti Server

Tekan `Ctrl + C` di terminal

---

<a name="semua-endpoint"></a>

# 📋 BAGIAN 3: SEMUA ENDPOINT DIJELASKAN

## Total: 26 Endpoint Baru

Dibagi menjadi 4 kategori:
- 🔐 Authentication & User (5 endpoint)
- 🌱 Farming Cycles (7 endpoint)
- 🍖 Feed Management (8 endpoint)
- 🤖 Machine Learning (6 endpoint)

---

## 🔐 KATEGORI 1: AUTENTIKASI & USER (5 Endpoint)

### Endpoint 1: REGISTER - Daftar Akun Baru

```
POST /auth/register
```

**Tujuan**: Membuat akun baru untuk user

**Data Masukan**:
```json
{
  "email": "petani@gmail.com",
  "password": "Rahasia123",
  "full_name": "Budi Santoso",
  "phone_number": "081234567890",
  "greenhouse_location": "Jakarta",
  "address": "Jl. Merdeka No. 1"
}
```

**Data Keluaran**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Penjelasan**:
- `access_token` = Tiket untuk menggunakan API (berlaku 60 menit)
- `refresh_token` = Tiket untuk mendapatkan token baru
- Setelah register, Anda langsung ter-login

**Contoh Kasus**: Pengguna pertama kali membuat akun

---

### Endpoint 2: LOGIN - Masuk Akun

```
POST /auth/login
```

**Tujuan**: Masuk dengan email dan password

**Data Masukan**:
```json
{
  "email": "petani@gmail.com",
  "password": "Rahasia123"
}
```

**Data Keluaran**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Penjelasan**:
- Sama seperti login di aplikasi biasa
- Password di-hash dengan bcrypt (aman)
- Mendapat token untuk menggunakan endpoint lain

**Contoh Kasus**: User mau masuk ke aplikasi lagi

---

### Endpoint 3: GET PROFILE - Lihat Data Profil Saya

```
GET /auth/me
```

**Tujuan**: Melihat data profil akun Anda sendiri

**Data Masukan**:
- Token (dari login)

**Data Keluaran**:
```json
{
  "id": 1,
  "email": "petani@gmail.com",
  "full_name": "Budi Santoso",
  "phone_number": "081234567890",
  "greenhouse_location": "Jakarta",
  "address": "Jl. Merdeka No. 1",
  "profile_photo_url": null,
  "created_at": "2024-01-15T10:30:00"
}
```

**Penjelasan**:
- Menampilkan semua data profil Anda
- `profile_photo_url` = URL foto (kosong jika belum upload)
- `created_at` = Tanggal akun dibuat

**Contoh Kasus**: User ingin lihat profil mereka sendiri

---

### Endpoint 4: UPDATE PROFILE - Ubah Data Profil

```
PUT /auth/me
```

**Tujuan**: Mengubah data profil (nama, telp, lokasi, alamat)

**Data Masukan** (pilih yang mau diubah):
```json
{
  "full_name": "Budi Santoso Baru",
  "phone_number": "082987654321",
  "greenhouse_location": "Bandung",
  "address": "Jl. Baru No. 2"
}
```

**Data Keluaran**:
```json
{
  "id": 1,
  "email": "petani@gmail.com",
  "full_name": "Budi Santoso Baru",
  "phone_number": "082987654321",
  "greenhouse_location": "Bandung",
  "address": "Jl. Baru No. 2",
  "updated_at": "2024-01-20T15:45:00"
}
```

**Penjelasan**:
- Ubah nama, nomor, lokasi, atau alamat
- Tidak perlu ubah semua, bisa salah satu atau lebih
- Email tidak bisa diubah (key unik)

**Contoh Kasus**: Pindah lokasi greenhouse

---

### Endpoint 5: UPLOAD FOTO PROFIL - Upload Foto

```
POST /auth/upload-photo
```

**Tujuan**: Upload foto profil

**Data Masukan**:
- Token
- File foto (jpg, png, dll)

**Data Keluaran**:
```json
{
  "message": "Photo uploaded successfully",
  "url": "/uploads/profile_photos/user_1_profil.jpg"
}
```

**Penjelasan**:
- Upload file foto dari komputer
- Foto disimpan di server
- URL foto disimpan di database

**Contoh Kasus**: User mau ubah foto profil

---

## 🌱 KATEGORI 2: FARMING CYCLES - Siklus Budidaya (7 Endpoint)

**Apa itu Farming Cycle?**
= Satu periode budidaya dari awal (penebaran benih) sampai panen.

**Contoh**:
- Siklus 1: 15 Jan 2024 - 25 Mar 2024 (panen)
- Siklus 2: 26 Mar 2024 - 05 Jun 2024 (panen)

---

### Endpoint 6: CREATE CYCLE - Buat Siklus Budidaya Baru

```
POST /farming-cycle/
```

**Tujuan**: Memulai siklus budidaya baru

**Data Masukan**:
```json
{
  "cycle_name": "Siklus Januari 2024",
  "seeding_date": "2024-01-15"
}
```

**Data Keluaran**:
```json
{
  "id": 1,
  "user_id": 1,
  "cycle_name": "Siklus Januari 2024",
  "seeding_date": "2024-01-15",
  "estimated_harvest_date": null,
  "actual_harvest_date": null,
  "status": "active",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Penjelasan**:
- `cycle_name` = Nama siklus (optional, bisa auto-generate)
- `seeding_date` = Tanggal penebaran benih (WAJIB)
- `status` = "active" (sedang berlangsung)
- `estimated_harvest_date` = Akan di-generate oleh AI nantinya

**Contoh Kasus**: Petani baru mau mulai budidaya

---

### Endpoint 7: LIST CYCLES - Lihat Semua Siklus

```
GET /farming-cycle/
```

**Tujuan**: Melihat daftar semua siklus budidaya Anda

**Data Masukan**:
- Token

**Data Keluaran**:
```json
[
  {
    "id": 1,
    "cycle_name": "Siklus Januari 2024",
    "seeding_date": "2024-01-15",
    "status": "active",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "cycle_name": "Siklus Desember 2023",
    "seeding_date": "2023-12-01",
    "status": "completed",
    "actual_harvest_date": "2024-02-10"
  }
]
```

**Penjelasan**:
- Menampilkan semua siklus (lama dan baru)
- `status` = "active" (berjalan) atau "completed" (selesai)

**Contoh Kasus**: Lihat riwayat budidaya semua siklus

---

### Endpoint 8: GET ACTIVE CYCLE - Lihat Siklus yang Sedang Berjalan

```
GET /farming-cycle/active
```

**Tujuan**: Melihat siklus budidaya yang SEDANG AKTIF saat ini

**Data Masukan**:
- Token

**Data Keluaran**:
```json
{
  "id": 1,
  "cycle_name": "Siklus Januari 2024",
  "seeding_date": "2024-01-15",
  "status": "active",
  "created_at": "2024-01-15T10:30:00"
}
```

**Penjelasan**:
- Hanya menampilkan 1 siklus yang paling baru (aktif)
- Gunakan ini untuk mendapat cycle_id dengan cepat

**Contoh Kasus**: Cek siklus apa yang lagi berjalan

---

### Endpoint 9: GET CYCLE DETAILS - Lihat Detail Siklus Tertentu

```
GET /farming-cycle/{id}
```

**Tujuan**: Melihat detail siklus yang spesifik

**Contoh**:
```
GET /farming-cycle/1
```

**Data Keluaran**:
```json
{
  "id": 1,
  "cycle_name": "Siklus Januari 2024",
  "seeding_date": "2024-01-15",
  "estimated_harvest_date": "2024-03-25",
  "actual_harvest_date": null,
  "status": "active",
  "created_at": "2024-01-15T10:30:00"
}
```

**Penjelasan**:
- `{id}` = Nomor siklus (1, 2, 3, dll)
- Menampilkan detail siklus yang diminta

**Contoh Kasus**: Lihat detail siklus no. 1

---

### Endpoint 10: UPDATE CYCLE - Ubah Status Siklus

```
PUT /farming-cycle/{id}
```

**Tujuan**: Mengubah status siklus atau mencatat tanggal panen

**Data Masukan**:
```json
{
  "status": "completed",
  "actual_harvest_date": "2024-03-20"
}
```

**Data Keluaran**:
```json
{
  "id": 1,
  "cycle_name": "Siklus Januari 2024",
  "seeding_date": "2024-01-15",
  "status": "completed",
  "actual_harvest_date": "2024-03-20",
  "updated_at": "2024-03-20T14:30:00"
}
```

**Penjelasan**:
- `status` = "planning" (perencanaan) → "active" → "harvesting" → "completed"
- `actual_harvest_date` = Tanggal panen sebenarnya

**Contoh Kasus**: Mencatat bahwa ikan sudah dipanen

---

### Endpoint 11: GET FARMING DAYS - Hitung Hari Budidaya

```
GET /farming-cycle/{id}/days
```

**Tujuan**: Hitung berapa hari sejak penebaran benih sampai hari ini

**Contoh**:
```
GET /farming-cycle/1/days
```

**Data Keluaran**:
```json
{
  "cycle_id": 1,
  "farming_days": 45,
  "seeding_date": "2024-01-15",
  "status": "active"
}
```

**Penjelasan**:
- `farming_days` = 45 hari (berarti sudah 45 hari sejak penebaran)
- Dihitung otomatis dari tanggal seeding sampai hari ini

**Contoh Kasus**: Tahu sudah berapa lama budidaya ini

---

### Endpoint 12: GET CYCLE STATS - Lihat Statistik Siklus

```
GET /farming-cycle/{id}/stats
```

**Tujuan**: Melihat statistik lengkap siklus

**Contoh**:
```
GET /farming-cycle/1/stats
```

**Data Keluaran**:
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

**Penjelasan**:
- `farming_days` = Sudah 45 hari budidaya
- `total_feeding_events` = Sudah 135 kali kasih pakan
- `total_feed_quantity` = Total 202.5 kg pakan diberikan
- `feeding_schedules` = Ada 3 jadwal pemberian pakan

**Contoh Kasus**: Lihat ringkasan statistik siklus

---

## 🍖 KATEGORI 3: FEED MANAGEMENT - Pakan (8 Endpoint)

**Apa itu Feed?** = Pakan untuk ikan/udang

**Alur**: Beli pakan → Simpan di gudang → Catat pemberian → Catat sisa

---

### Endpoint 13: LIST FEED STOCKS - Lihat Semua Stok Pakan

```
GET /feed/stocks
```

**Tujuan**: Melihat daftar semua stok pakan Anda

**Data Keluaran**:
```json
[
  {
    "id": 1,
    "current_quantity": 60,
    "unit": "kg",
    "min_threshold": 20,
    "farming_cycle_id": 1,
    "updated_at": "2024-01-20T15:00:00"
  }
]
```

**Penjelasan**:
- `current_quantity` = 60 kg (stok sekarang)
- `unit` = Satuan (kg)
- `min_threshold` = 20 kg (minimum yang boleh)
- `farming_cycle_id` = Untuk siklus no. 1

**Contoh Kasus**: Cek stok pakan sekarang berapa

---

### Endpoint 14: GET FEED STOCK FOR CYCLE - Lihat Stok Pakan Siklus Tertentu

```
GET /feed/stocks/{cycle_id}
```

**Tujuan**: Lihat stok pakan untuk siklus tertentu

**Contoh**:
```
GET /feed/stocks/1
```

**Data Keluaran**:
```json
{
  "id": 1,
  "current_quantity": 60,
  "unit": "kg",
  "min_threshold": 20,
  "farming_cycle_id": 1,
  "updated_at": "2024-01-20T15:00:00"
}
```

**Contoh Kasus**: Cek stok pakan untuk siklus Januari

---

### Endpoint 15: RECORD FEED TRANSACTION - Catat Transaksi Pakan

```
POST /feed/stocks/{id}/transaction
```

**Tujuan**: Mencatat transaksi pakan (beli atau kasih ke ikan)

#### **Contoh 1: BELI PAKAN (INPUT)**

```
POST /feed/stocks/1/transaction
```

**Data Masukan**:
```json
{
  "transaction_type": "input",
  "quantity": 50,
  "notes": "Beli pakan 1 sak 50kg di toko Mitra Jaya"
}
```

**Data Keluaran**:
```json
{
  "id": 1,
  "feed_stock_id": 1,
  "transaction_type": "input",
  "quantity": 50,
  "notes": "Beli pakan 1 sak 50kg di toko Mitra Jaya",
  "previous_quantity": 10,
  "new_quantity": 60,
  "created_at": "2024-01-20T15:00:00"
}
```

**Penjelasan**:
- `transaction_type` = "input" (beli/masuk)
- Stok berubah dari 10kg → 60kg (10 + 50)
- Semua perubahan tercatat otomatis

#### **Contoh 2: KASIH PAKAN KE IKAN (USAGE)**

```
POST /feed/stocks/1/transaction
```

**Data Masukan**:
```json
{
  "transaction_type": "usage",
  "quantity": 5,
  "notes": "Pagi pemberian pakan normal, ikan lapar"
}
```

**Data Keluaran**:
```json
{
  "id": 2,
  "feed_stock_id": 1,
  "transaction_type": "usage",
  "quantity": 5,
  "notes": "Pagi pemberian pakan normal, ikan lapar",
  "previous_quantity": 60,
  "new_quantity": 55,
  "created_at": "2024-01-20T16:00:00"
}
```

**Penjelasan**:
- `transaction_type` = "usage" (dipakai/keluar)
- Stok berubah dari 60kg → 55kg (60 - 5)

**Contoh Kasus**: Catat beli pakan atau kasih pakan ke ikan

---

### Endpoint 16: GET FEED HISTORY - Lihat Riwayat Transaksi Pakan

```
GET /feed/stocks/{id}/history
```

**Tujuan**: Melihat semua riwayat transaksi pakan

**Contoh**:
```
GET /feed/stocks/1/history
```

**Data Keluaran**:
```json
[
  {
    "id": 2,
    "transaction_type": "usage",
    "quantity": 5,
    "previous_quantity": 60,
    "new_quantity": 55,
    "notes": "Pagi pemberian pakan normal",
    "created_at": "2024-01-20T16:00:00"
  },
  {
    "id": 1,
    "transaction_type": "input",
    "quantity": 50,
    "previous_quantity": 10,
    "new_quantity": 60,
    "notes": "Beli pakan 1 sak 50kg",
    "created_at": "2024-01-20T15:00:00"
  }
]
```

**Penjelasan**:
- Semua transaksi tercatat chronologically (terbaru di atas)
- Bisa tracking stok dari waktu ke waktu

**Contoh Kasus**: Audit riwayat pakan

---

### Endpoint 17: GET FEED STATS - Lihat Statistik Pakan

```
GET /feed/stocks/{id}/stats
```

**Tujuan**: Melihat statistik pakan (total input, total dipakai, balance)

**Contoh**:
```
GET /feed/stocks/1/stats
```

**Data Keluaran**:
```json
{
  "stock_id": 1,
  "current_quantity": 55,
  "unit": "kg",
  "total_input": 110,
  "total_usage": 55,
  "transaction_count": 10,
  "min_threshold": 20,
  "below_threshold": false
}
```

**Penjelasan**:
- `current_quantity` = 55 kg (stok sekarang)
- `total_input` = 110 kg (total pakan yang pernah dibeli)
- `total_usage` = 55 kg (total pakan yang pernah diberikan)
- `below_threshold` = false (stok masih aman, tidak kurang dari 20kg)

**Contoh Kasus**: Laporan statistik pakan bulanan

---

### Endpoint 18: CREATE FEEDING SCHEDULE - Buat Jadwal Pemberian Pakan

```
POST /feed/schedule/{cycle_id}
```

**Tujuan**: Membuat jadwal pemberian pakan yang teratur

**Contoh**:
```
POST /feed/schedule/1
```

**Data Masukan**:
```json
{
  "scheduled_time": "07:00",
  "expected_quantity": 5,
  "frequency": "daily"
}
```

**Data Keluaran**:
```json
{
  "id": 1,
  "farming_cycle_id": 1,
  "scheduled_time": "07:00",
  "expected_quantity": 5,
  "frequency": "daily",
  "status": "active",
  "created_at": "2024-01-20T15:00:00"
}
```

**Penjelasan**:
- `scheduled_time` = Jam 07:00 (pukul 7 pagi)
- `expected_quantity` = 5 kg (berapa banyak yang akan diberikan)
- `frequency` = "daily" (setiap hari)
- Jadwal bisa diisi berapa kali (pagi, siang, sore, malam)

**Contoh Kasus**: Buat jadwal pemberian pakan 3x sehari

---

### Endpoint 19: LIST FEEDING SCHEDULES - Lihat Jadwal Pemberian Pakan

```
GET /feed/schedule/{cycle_id}
```

**Tujuan**: Melihat semua jadwal pemberian pakan untuk siklus

**Contoh**:
```
GET /feed/schedule/1
```

**Data Keluaran**:
```json
[
  {
    "id": 1,
    "farming_cycle_id": 1,
    "scheduled_time": "07:00",
    "expected_quantity": 5,
    "frequency": "daily",
    "status": "active",
    "created_at": "2024-01-20T15:00:00"
  },
  {
    "id": 2,
    "farming_cycle_id": 1,
    "scheduled_time": "12:00",
    "expected_quantity": 5,
    "frequency": "daily",
    "status": "active",
    "created_at": "2024-01-20T15:05:00"
  },
  {
    "id": 3,
    "farming_cycle_id": 1,
    "scheduled_time": "17:00",
    "expected_quantity": 5,
    "frequency": "daily",
    "status": "active",
    "created_at": "2024-01-20T15:10:00"
  }
]
```

**Penjelasan**:
- Ada 3 jadwal pemberian pakan per hari
- Pagi (07:00), Siang (12:00), Sore (17:00)
- Setiap jadwal 5 kg per pemberian

**Contoh Kasus**: Lihat semua jadwal pemberian pakan siklus ini

---

### Endpoint 20: RECORD FEEDING - Catat Pemberian Pakan Sebenarnya

```
POST /feed/history/{cycle_id}
```

**Tujuan**: Mencatat pemberian pakan yang sudah dilakukan

**Contoh**:
```
POST /feed/history/1
```

**Data Masukan**:
```json
{
  "feeding_schedule_id": 1,
  "quantity_given": 5.2,
  "administered_by": "system",
  "notes": "Pagi, ikan lapar, semua habis dalam 5 menit"
}
```

**Data Keluaran**:
```json
{
  "id": 1,
  "feeding_schedule_id": 1,
  "farming_cycle_id": 1,
  "actual_time": "2024-01-20T07:15:00",
  "quantity_given": 5.2,
  "administered_by": "system",
  "notes": "Pagi, ikan lapar, semua habis dalam 5 menit",
  "created_at": "2024-01-20T07:15:00"
}
```

**Penjelasan**:
- `quantity_given` = 5.2 kg (berapa yang benar-benar diberikan)
- `administered_by` = "system" (siapa yang kasih, bisa manual atau otomatis)
- `actual_time` = Waktu pemberian sebenarnya (auto-recorded)

**Contoh Kasus**: Catat pemberian pakan yang sudah dilakukan

---

### Endpoint 21: GET FEEDING HISTORY - Lihat Riwayat Pemberian Pakan

```
GET /feed/history/{cycle_id}
```

**Tujuan**: Melihat semua riwayat pemberian pakan

**Contoh**:
```
GET /feed/history/1
```

**Data Keluaran**:
```json
[
  {
    "id": 135,
    "feeding_schedule_id": 3,
    "actual_time": "2024-01-20T17:00:00",
    "quantity_given": 4.9,
    "notes": "Sore"
  },
  {
    "id": 134,
    "feeding_schedule_id": 2,
    "actual_time": "2024-01-20T12:05:00",
    "quantity_given": 4.8,
    "notes": "Siang"
  },
  {
    "id": 133,
    "feeding_schedule_id": 1,
    "actual_time": "2024-01-20T07:15:00",
    "quantity_given": 5.2,
    "notes": "Pagi, ikan lapar"
  }
]
```

**Penjelasan**:
- Semua pemberian pakan tercatat dengan timestamp
- Bisa tracking konsistensi pemberian pakan
- 135 event berarti sudah 135 kali kasih pakan

**Contoh Kasus**: Lihat riwayat pemberian pakan

---

### Endpoint 22: GET FEEDING STATS - Lihat Statistik Pemberian Pakan

```
GET /feed/history/{cycle_id}/stats
```

**Tujuan**: Melihat statistik pemberian pakan (total event, rata-rata)

**Contoh**:
```
GET /feed/history/1/stats
```

**Data Keluaran**:
```json
{
  "farming_cycle_id": 1,
  "total_feeding_events": 135,
  "total_feed_quantity": 202.5,
  "average_per_feeding": 1.5,
  "active_schedules": 3
}
```

**Penjelasan**:
- `total_feeding_events` = 135 kali pemberian
- `total_feed_quantity` = 202.5 kg total yang diberikan
- `average_per_feeding` = 1.5 kg rata-rata per pemberian
- `active_schedules` = 3 jadwal aktif

**Contoh Kasus**: Laporan statistik pemberian pakan

---

## 🤖 KATEGORI 4: MACHINE LEARNING - Prediksi AI (6 Endpoint)

**Apa itu ML?** = Kecerdasan buatan yang belajar dari data Anda

**Bagaimana cara kerjanya?**
1. Sistem kumpulkan data (hari budidaya, kualitas air, pakan yang diberikan)
2. AI analisis pola dari data
3. AI prediksi / rekomendasikan sesuatu

---

### Endpoint 23: HARVEST PREDICTION - Prediksi Kapan Panen

```
POST /ml/harvest-estimate/{cycle_id}
```

**Tujuan**: AI memberikan prediksi kapan waktu terbaik untuk panen

**Contoh**:
```
POST /ml/harvest-estimate/1
```

**Data Keluaran**:
```json
{
  "id": 1,
  "farming_cycle_id": 1,
  "predicted_harvest_date": "2024-03-25",
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
  "prediction_date": "2024-01-20T15:00:00"
}
```

**Penjelasan**:
- `predicted_harvest_date` = 25 Maret 2024 (prediksi tanggal panen)
- `confidence_score` = 85.5% (AI 85.5% yakin dengan prediksi ini)
- `features_used` = Data yang digunakan AI untuk prediksi:
  - Sudah 45 hari budidaya
  - Rata-rata TDS: 420.5 ppm
  - Rata-rata pH: 7.2
  - Rata-rata DO: 6.8 mg/L
  - Rata-rata suhu: 27.5°C
  - Total pakan diberikan: 202.5 kg
  - Rata-rata pakan per hari: 4.5 kg
  - Ada 180 data sensor

**Contoh Kasus**: Petani mau tahu kapan waktu panen

---

### Endpoint 24: LIST HARVEST PREDICTIONS - Lihat Semua Prediksi Panen

```
GET /ml/harvest-estimate/{cycle_id}
```

**Tujuan**: Melihat semua prediksi panen yang pernah di-generate

**Contoh**:
```
GET /ml/harvest-estimate/1
```

**Data Keluaran**:
```json
[
  {
    "predicted_harvest_date": "2024-03-25",
    "confidence_score": 85.5,
    "prediction_date": "2024-01-20T15:00:00"
  },
  {
    "predicted_harvest_date": "2024-03-26",
    "confidence_score": 84.2,
    "prediction_date": "2024-01-19T14:00:00"
  },
  {
    "predicted_harvest_date": "2024-03-28",
    "confidence_score": 82.1,
    "prediction_date": "2024-01-18T13:00:00"
  }
]
```

**Penjelasan**:
- Prediksi bisa dijalankan berkali-kali
- Setiap prediksi baru akan akurat karena lebih banyak data
- Confidence score meningkat seiring waktu

**Contoh Kasus**: Lihat trend prediksi panen (apakah semakin dekat atau mundur)

---

### Endpoint 25: FEEDING RECOMMENDATION - Rekomendasi Jumlah & Waktu Pakan

```
POST /ml/feeding-recommend/{cycle_id}
```

**Tujuan**: AI merekomendasikan berapa banyak pakan & kapan memberinya

**Contoh**:
```
POST /ml/feeding-recommend/1
```

**Data Keluaran**:
```json
{
  "id": 1,
  "farming_cycle_id": 1,
  "recommended_quantity": 4.8,
  "recommended_time": "07:00",
  "reasoning": "Berdasarkan water temp 27.5°C, DO 6.8 mg/L, dan farming stage (45 hari)",
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
  "recommendation_date": "2024-01-20T15:05:00"
}
```

**Penjelasan**:
- `recommended_quantity` = 4.8 kg (rekomendasikan kasih 4.8kg)
- `recommended_time` = 07:00 (waktu terbaik: jam 7 pagi)
- `confidence_score` = 82.3% (AI 82.3% yakin)
- `reasoning` = Alasan AI:
  - Suhu air 27.5°C (ideal untuk pemberian pakan lebih banyak)
  - Oksigen terlarut 6.8 mg/L (baik)
  - Sudah hari ke-45 budidaya (fase growth)

**Contoh Kasus**: Petani bingung berapa banyak pakan yang harus diberikan

---

### Endpoint 26: LIST FEEDING RECOMMENDATIONS - Lihat Semua Rekomendasi

```
GET /ml/feeding-recommend/{cycle_id}
```

**Tujuan**: Melihat semua rekomendasi pakan yang pernah di-generate

**Contoh**:
```
GET /ml/feeding-recommend/1
```

**Data Keluaran**:
```json
[
  {
    "recommended_quantity": 4.8,
    "recommended_time": "07:00",
    "confidence_score": 82.3,
    "recommendation_date": "2024-01-20T15:05:00"
  },
  {
    "recommended_quantity": 4.7,
    "recommended_time": "07:00",
    "confidence_score": 81.5,
    "recommendation_date": "2024-01-19T14:05:00"
  }
]
```

**Penjelasan**:
- Rekomendasi bisa berubah setiap hari sesuai kondisi air
- AI semakin pintar karena semakin banyak data

**Contoh Kasus**: Lihat trend rekomendasi pakan harian

---

### Endpoint 27: LIST ACTIVE MODELS - Lihat Model AI yang Sedang Aktif

```
GET /ml/models
```

**Tujuan**: Melihat AI model apa yang sedang digunakan dan akurasi mereka

**Data Keluaran**:
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

**Penjelasan**:
- Ada 2 model AI yang aktif
- **Harvest Estimation Model** = Prediksi panen (akurasi 85%)
- **Feeding Decision Model** = Rekomendasi pakan (akurasi 80%)
- Akurasi akan meningkat seiring waktu

**Contoh Kasus**: Admin mau cek model AI yang mana yang aktif

---

### Endpoint 28: GET MODEL PERFORMANCE - Lihat Performa Model

```
GET /ml/models/{id}/performance
```

**Tujuan**: Melihat detail performa model AI

**Contoh**:
```
GET /ml/models/1/performance
```

**Data Keluaran**:
```json
{
  "model_id": 1,
  "model_type": "harvest_estimation",
  "version": "v1.0",
  "total_predictions": 45,
  "avg_confidence": 83.2,
  "accuracy": 85.0
}
```

**Penjelasan**:
- `model_id` = ID model
- `model_type` = Tipe model (harvest_estimation atau feeding_decision)
- `version` = Versi model (v1.0)
- `total_predictions` = 45 kali sudah memprediksi
- `avg_confidence` = Rata-rata confidence score: 83.2%
- `accuracy` = Akurasi model: 85% (seberapa sering prediksi benar)

**Contoh Kasus**: Admin mau tahu seberapa akurat model AI

---

<a name="contoh-real"></a>

# 🎯 BAGIAN 4: CONTOH PENGGUNAAN REAL (Skenario Nyata)

## Skenario Lengkap: Petani Mulai Budidaya dari Nol

### **HARI PERTAMA - PERSIAPAN PENEBARAN**

#### Step 1: Register Akun
```
Endpoint: POST /auth/register

Masukan:
  email: budi@gmail.com
  password: Rahasia123
  full_name: Budi Santoso
  greenhouse_location: Jakarta

Hasil:
  access_token: "eyJhbGc..."
  (Simpan token ini untuk nanti)
```

#### Step 2: Login
```
Endpoint: POST /auth/login

Masukan:
  email: budi@gmail.com
  password: Rahasia123

Hasil:
  access_token: "eyJhbGc..." (sama seperti register)
```

#### Step 3: Lihat Profil
```
Endpoint: GET /auth/me

Hasil:
  id: 1
  email: budi@gmail.com
  full_name: Budi Santoso
  greenhouse_location: Jakarta
```

#### Step 4: Mulai Siklus Budidaya Pertama
```
Endpoint: POST /farming-cycle/

Masukan:
  cycle_name: "Siklus Januari 2024"
  seeding_date: "2024-01-15"

Hasil:
  id: 1 (Cycle ID - simpan ini!)
  status: "active"
```

#### Step 5: Beli Pakan
```
Endpoint: POST /feed/stocks/1/transaction

Masukan:
  transaction_type: "input"
  quantity: 100
  notes: "Beli pakan 2 sak dari PT Mitra"

Hasil:
  stock_id: 1
  previous_quantity: 0
  new_quantity: 100
  (Sekarang stok 100kg)
```

#### Step 6: Buat Jadwal Pemberian Pakan 3x Sehari
```
Endpoint 1: POST /feed/schedule/1
Masukan:
  scheduled_time: "07:00"
  expected_quantity: 5
  frequency: "daily"

Endpoint 2: POST /feed/schedule/1
Masukan:
  scheduled_time: "12:00"
  expected_quantity: 5
  frequency: "daily"

Endpoint 3: POST /feed/schedule/1
Masukan:
  scheduled_time: "17:00"
  expected_quantity: 5
  frequency: "daily"

Hasil:
  3 jadwal pemberian pakan sudah dibuat
```

---

### **HARI 2-45 - PEMELIHARAAN**

#### Setiap Pagi:
```
Endpoint: POST /feed/history/1

Masukan:
  feeding_schedule_id: 1
  quantity_given: 5.1
  notes: "Pagi, ikan sehat"

Hasil:
  Pemberian pakan tercatat
```

#### Setiap Siang:
```
Endpoint: POST /feed/history/1

Masukan:
  feeding_schedule_id: 2
  quantity_given: 5.0
  notes: "Siang, normal"
```

#### Setiap Sore:
```
Endpoint: POST /feed/history/1

Masukan:
  feeding_schedule_id: 3
  quantity_given: 4.9
  notes: "Sore, normal"
```

#### Setiap Minggu: Cek Statistik
```
Endpoint: GET /feed/history/1/stats

Hasil:
  total_feeding_events: 21 (3x sehari x 7 hari)
  total_feed_quantity: 105 kg
  average_per_feeding: 5 kg
```

#### Setiap Hari: Prediksi Panen dari AI
```
Endpoint: POST /ml/harvest-estimate/1

Hasil (hari ke-10):
  predicted_harvest_date: "2024-03-28"
  confidence_score: 60% (masih rendah, data sedikit)

Hasil (hari ke-30):
  predicted_harvest_date: "2024-03-25"
  confidence_score: 82% (lebih akurat, data banyak)

Hasil (hari ke-45):
  predicted_harvest_date: "2024-03-25"
  confidence_score: 85% (tinggi, data lengkap)
```

#### Setiap Hari: Rekomendasi Pakan dari AI
```
Endpoint: POST /ml/feeding-recommend/1

Hasil:
  recommended_quantity: 4.8 kg
  recommended_time: "07:00"
  confidence_score: 82.3%
  reasoning: "Suhu air bagus, oksigen cukup"
```

---

### **HARI 45 - PANEN**

#### Step 1: Cek Hari Budidaya
```
Endpoint: GET /farming-cycle/1/days

Hasil:
  farming_days: 45
  (Sudah 45 hari, waktunya panen!)
```

#### Step 2: Lihat Prediksi Panen
```
Endpoint: GET /ml/harvest-estimate/1

Hasil:
  predicted_harvest_date: "2024-03-25"
  actual_date_today: "2024-03-25"
  (Prediksi tepat! Waktu panen sekarang!)
```

#### Step 3: Catat Panen
```
Endpoint: PUT /farming-cycle/1

Masukan:
  status: "completed"
  actual_harvest_date: "2024-03-25"

Hasil:
  status: "completed"
  (Siklus selesai, siap mulai siklus baru!)
```

#### Step 4: Lihat Statistik Akhir Siklus
```
Endpoint: GET /farming-cycle/1/stats

Hasil:
  farming_days: 45
  total_feeding_events: 135
  total_feed_quantity: 202.5 kg
  (Laporan lengkap untuk evaluasi)
```

#### Step 5: Mulai Siklus Baru
```
Endpoint: POST /farming-cycle/

Masukan:
  cycle_name: "Siklus Februari 2024"
  seeding_date: "2024-03-26"

Hasil:
  id: 2
  status: "active"
  (Siap mulai budidaya baru!)
```

---

<a name="tips"></a>

# 💡 BAGIAN 5: TIPS & TRIK

## Tips Menggunakan Endpoint

### Tip 1: Selalu Simpan Token
```
Saat login/register, Anda dapat token:
  access_token: "eyJhbGc..."

SIMPAN TOKEN INI! Digunakan di semua endpoint lain.
```

### Tip 2: Gunakan Cycle ID
```
Saat membuat siklus:
  id: 1

Gunakan ID ini untuk:
  - GET /farming-cycle/1/stats
  - POST /feed/schedule/1
  - POST /ml/harvest-estimate/1
  dll

Jadi hafal cycle ID Anda!
```

### Tip 3: Refresh Prediksi Setiap Hari
```
Jangan jalankan prediksi hanya sekali.
Jalankan setiap hari untuk perkiraan yang lebih akurat:
  POST /ml/harvest-estimate/1  (hari ke-10)
  POST /ml/harvest-estimate/1  (hari ke-20)
  POST /ml/harvest-estimate/1  (hari ke-30)
  dll

Akurasi akan meningkat!
```

### Tip 4: Konsisten Mencatat Pemberian Pakan
```
Semakin konsisten catat pemberian pakan,
semakin akurat prediksi dan rekomendasi AI.

JANGAN LUPA catat setiap kali kasih pakan!
```

### Tip 5: Perhatikan Rekomendasi AI
```
Sebelum memberi pakan, cek rekomendasi:
  POST /ml/feeding-recommend/1

Ikuti rekomendasi AI untuk hasil optimal.
```

---

## Tips Troubleshooting

### Masalah: Token Expired
```
Error: Invalid or expired token

Solusi:
  1. Login lagi
  2. Ambil token baru
  3. Gunakan token baru di semua endpoint
```

### Masalah: Insufficient Feed Stock
```
Error: Insufficient feed stock. Available: 10, Requested: 50

Solusi:
  1. Beli pakan baru lebih dulu
  2. Atau catat pemberian pakan lebih sedikit
```

### Masalah: Cycle Not Found
```
Error: Farming cycle not found

Solusi:
  1. Buat siklus baru dulu dengan POST /farming-cycle/
  2. Atau gunakan cycle ID yang benar
```

---

<a name="troubleshooting"></a>

# 🔧 BAGIAN 6: TROUBLESHOOTING

## Masalah Umum & Solusi

### Masalah 1: Backend Tidak Bisa Dijalankan

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solusi**:
```bash
# Cek virtual environment aktif (cari (venv) di prompt)
venv\Scripts\activate

# Install ulang dependencies
pip install -r requirements.txt

# Jalankan lagi
uvicorn app.main:app --reload
```

---

### Masalah 2: Database Connection Failed

**Error**: `ERROR: Database connection failed`

**Solusi**:
```bash
# Pastikan PostgreSQL running
# Jalankan init script lagi
python init_app_db.py

# Atau cek .env file
# DATABASE_URL harus benar
```

---

### Masalah 3: Port 8000 Sudah Terpakai

**Error**: `Address already in use`

**Solusi**:
```bash
# Jalankan di port lain
uvicorn app.main:app --reload --port 8001

# Buka di browser
http://localhost:8001/docs
```

---

### Masalah 4: Endpoint Return Error 401

**Error**: `detail: "Invalid or expired token"`

**Solusi**:
```
Token Anda expired (lebih dari 60 menit)
Login lagi untuk dapat token baru
```

---

### Masalah 5: Register Email Sudah Ada

**Error**: `detail: "Email already registered"`

**Solusi**:
```
Email sudah terdaftar
Gunakan email berbeda atau login dengan email tersebut
```

---

## FAQ - Pertanyaan Sering Diajukan

### Q: Berapa lama token berlaku?
**A**: 60 menit. Setelah itu, harus login lagi.

### Q: Apa itu confidence score di ML?
**A**: Tingkat kepercayaan AI terhadap prediksi (0-100%). Semakin tinggi semakin akurat.

### Q: Berapa akurasi AI?
**A**: 
- Harvest Estimation: ~85%
- Feeding Recommendation: ~80%
Akurasi meningkat seiring bertambahnya data.

### Q: Bisa ganti password?
**A**: Belum ada endpoint untuk itu. Hubungi admin.

### Q: Berapa maximum user?
**A**: Unlimited! Bisa tambah user sebanyak mungkin.

### Q: Data bisa dihapus?
**A**: Belum ada endpoint delete. Hubungi admin jika perlu hapus data.

### Q: Bisa backup database?
**A**: Ya, pakai pgAdmin 4 atau command line PostgreSQL.

### Q: Bisa akses dari mobile?
**A**: Ya! API ini dirancang untuk mobile (Flutter/React).

---

# 📞 RINGKASAN CEPAT

## Workflow Singkat

```
1. Register/Login
   ↓
2. Buat Farming Cycle
   ↓
3. Beli & catat pakan
   ↓
4. Buat jadwal pemberian
   ↓
5. Catat pemberian pakan setiap hari
   ↓
6. Lihat prediksi panen dari AI setiap hari
   ↓
7. Panen saat waktu tiba
   ↓
8. Mulai siklus baru
```

## Endpoint Paling Penting

| Fungsi | Endpoint |
|--------|----------|
| Mulai | POST /auth/register |
| Masuk | POST /auth/login |
| Buat siklus | POST /farming-cycle/ |
| Catat pakan | POST /feed/stocks/{id}/transaction |
| Catat pemberian | POST /feed/history/{id} |
| Prediksi panen | POST /ml/harvest-estimate/{id} |
| Rekomendasi pakan | POST /ml/feeding-recommend/{id} |

## Total Endpoint

- **Authentication**: 5 endpoint
- **Farming**: 7 endpoint
- **Feed**: 8 endpoint
- **ML**: 6 endpoint
- **TOTAL: 26 endpoint** ✅

---

# ✨ SELESAI!

Sekarang Anda sudah tahu:
✅ Apa itu Backend NILA
✅ Cara menjalankan
✅ Semua 26 endpoint
✅ Contoh penggunaan real
✅ Tips & trick
✅ Troubleshooting

**Selamat mencoba Backend NILA! 🚀**

Buka browser → http://localhost:8000/docs → Mulai explore!

---

**Dokumen ini dibuat untuk memudahkan Anda memahami dan menggunakan Backend NILA.**

Jika ada pertanyaan, lihat kembali bagian yang relevan di dokumen ini.

**Terima kasih!** 🙏
