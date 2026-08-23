# Incident Management Backend System

🚀 Cara Menjalankan Aplikasi

Menggunakan Docker

Sistem sudah sepenuhnya Dockerized. Jalankan perintah ini di terminal:

docker-compose up --build

🧪 Cara Menjalankan Test

Jalankan perintah berikut di terminal:

python -m pytest -v

⚙️ Environment Variables

# URL koneksi untuk aplikasi lokal
DATABASE_URL=postgresql://postgres:reihan123@localhost:5432/incident_db

# Kredensial untuk inisialisasi Docker Compose
DB_USER=postgres
DB_PASSWORD=reihan123
DB_NAME=incident_db

🏗️ Arsitektur Singkat

Project ini menerapkan **Layered Architecture** (Separation of Concerns) agar sistem modular, mudah di-maintain, dan mudah diuji:
* **API Layer (`app/api/`):** Menangani lalu lintas HTTP (Request/Response) dan validasi skema data menggunakan Pydantic.
* **Service Layer (`app/services/`):** Memuat *core business logic*, kalkulasi prioritas berdasarkan *keyword*, klasifikasi kategori via ML, dan pemicu *background tasks*.
* **Repository Layer (`app/repositories/`):** Mengelola interaksi dengan *database* PostgreSQL menggunakan pola *Repository Pattern* dan SQLAlchemy ORM.
* **Dependency Injection:** Dikelola penuh oleh FastAPI untuk mendistribusikan instansiasi *database* dan *service* secara aman.

🌐 API Endpoint

Sistem ini mengekspos endpoint utama untuk pembuatan insiden:
- POST /api/v1/incidents
  - Payload (JSON): Membutuhkan title (string), description (string), dan reported_by (string/email).
  - Response (201 Created): Mengembalikan data insiden lengkap dengan id, priority (dihitung otomatis), category (hasil prediksi ML), status (OPEN), dan created_at.

🤖 Pendekatan Machine Learning

Klasifikasi kategori tiket (ACCESS, DATABASE, PAYMENT, NETWORK, OTHER) diselesaikan menggunakan algoritma Multinomial Naive Bayes dikombinasikan dengan TF-IDF Vectorizer via scikit-learn.

⚖️ Asumsi dan Trade-off

1. Notifikasi Asinkron: Pengiriman notifikasi berjalan menggunakan BackgroundTasks bawaan FastAPI.
2. Notification Service Eksternal: Diasumsikan sebagai layanan HTTP terpisah. Kegagalan service ini telah diisolasi (ditangkap menggunakan blok try-except & logger) agar tidak memblokir dan menggagalkan respons API utama.
3. Pemuatan Model ML: File model .pkl dimuat ke dalam memori saat inisiasi Service.
