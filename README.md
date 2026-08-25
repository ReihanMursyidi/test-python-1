# Incident Management Backend System

Backend system untuk mengelola insiden, dibangun menggunakan FastAPI, PostgreSQL, SQLAlchemy, dan scikit-learn.

## 🚀 Cara Menjalankan Aplikasi

### 1. Menggunakan Docker

Sistem sudah sepenuhnya menggunakan Docker. Jalankan perintah berikut di terminal:

```bash
docker compose up --build
```

### 2. Menggunakan Server Lokal

Jika ingin menjalankan aplikasi secara lokal, buat virtual environment:

```bash
python -m venv venv
```

Aktifkan virtual environment:

```bash
venv\Scripts\activate
```

Install seluruh dependensi:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi menggunakan Uvicorn:

```bash
uvicorn app.main:app --reload
```

Aplikasi dapat diakses melalui `http://localhost:8000`.

Dokumentasi API tersedia di `http://localhost:8000/docs`.

## 🧪 Cara Menjalankan Test

Jalankan perintah berikut:

```bash
python -m pytest -v
```

## ⚙️ Environment Variables

Untuk menjaga keamanan, kredensial database tidak disimpan di dalam source code.
Inisialisasikan environment variables sebelum menjalankan aplikasi dengan Docker.

1. Salin template `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

2. Buka file `.env`, lalu isi variabel sesuai kebutuhan. Contoh:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=masukkan_password_anda_di_sini
POSTGRES_DB=incident_db
```
> **Catatan:** File `.env` seharusnya tercantum dalam `.gitignore` agar tidak terunggah ke repositori.

## 🏗️ Arsitektur Singkat

Project ini menerapkan **Layered Architecture** gar sistem modular, mudah di-maintain, dan mudah diuji:

- **API Layer (`app/api/`):** Menangani lalu lintas HTTP, request/response, dan validasi skema menggunakan Pydantic.
- **Service Layer (`app/services/`):** Menangani business logic, kalkulasi prioritas berbasis keyword, klasifikasi kategori berbasis ML, dan background task.
- **Repository Layer (`app/repositories/`):** Mengelola interaksi dengan PostgreSQL menggunakan Repository Pattern dan SQLAlchemy ORM.
- **Dependency Injection:** Dikelola oleh FastAPI untuk menyediakan instance database dan service secara terstruktur.

## 🌐 API Endpoint

### Membuat Insiden

```http
POST /api/v1/incidents
Content-Type: application/json
```

#### Request Body

```json
{
  "title": "Tidak dapat mengakses aplikasi",
  "description": "Pengguna gagal masuk ke aplikasi sejak pagi.",
  "reported_by": "user@example.com"
}
```

Field yang diperlukan:

- `title`: Judul insiden berupa string.
- `description`: Deskripsi insiden berupa string.
- `reported_by`: Identitas atau alamat email pelapor.

#### Response `201 Created`

Mengembalikan data insiden lengkap dengan `id`, `priority`, `category`, `status`, dan `created_at`.

Nilai `priority` dihitung secara otomatis, sedangkan `category` diprediksi oleh model ML. Status awal insiden adalah `OPEN`.

## 🤖 Pendekatan Machine Learning

Klasifikasi kategori tiket (`ACCESS`, `DATABASE`, `PAYMENT`, `NETWORK`, dan `OTHER`) menggunakan **Multinomial Naive Bayes** yang dikombinasikan dengan **TF-IDF Vectorizer** dari scikit-learn.

Jalankan perintah berikut untuk menghasilkan model:

```bash
python scripts/train_model.py
```

## ⚖️ Asumsi dan Trade-off

1. **Notifikasi asinkron:** Pengiriman notifikasi menggunakan `BackgroundTasks` bawaan FastAPI.
2. **Notification service eksternal:** Layanan notifikasi diasumsikan tersedia sebagai service HTTP terpisah. Kegagalannya diisolasi menggunakan `try-except` dan logger agar tidak menggagalkan respons API utama.
3. **Pemuatan model ML:** File model `.pkl` dimuat ke memori saat service diinisialisasi.
