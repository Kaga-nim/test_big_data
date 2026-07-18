# Sistem Manajemen Data Akademik

REST API berbasis **FastAPI** untuk mengelola data mahasiswa, mata kuliah, dan nilai. Dibangun sebagai proyek mata kuliah Algoritma & Pemrograman II dengan dukungan big data (1 juta data mahasiswa, 10 juta data nilai).

## Fitur

- CRUD data mahasiswa, mata kuliah, dan nilai via REST API
- Koneksi ke **SQL Server** menggunakan `pyodbc`
- Sinkronisasi data dengan file Excel (`mahasiswa.xlsx`)
- Script generator data dummy untuk pengujian skala besar

## Struktur Proyek

```
.
├── main.py                  # Aplikasi FastAPI (entry point)
├── requirements.txt         # Dependensi Python
├── .env.example             # Template konfigurasi database
└── scripts/
    ├── dummymahasiswa.py    # Generate 1 juta data mahasiswa ke Excel
    ├── import_data_excel.py # Import Excel ke tabel mahasiswa di SQL Server
    ├── dummynilai.py        # Generate 10 juta data nilai ke SQL Server
    └── dummymatakuliah.py   # Generate data mata kuliah ke SQL Server
```

## Prasyarat

- Python 3.10+
- SQL Server (Express atau versi lain)
- ODBC Driver 17 for SQL Server — [unduh di sini](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

## Setup

### 1. Clone repositori

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2. Buat virtual environment dan install dependensi

```bash
python -m venv myvenv
myvenv\Scripts\activate      # Windows
# atau: source myvenv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. Konfigurasi database

Salin `.env.example` menjadi `.env` lalu sesuaikan dengan konfigurasi SQL Server kamu:

```bash
copy .env.example .env
```

Isi file `.env`:

```env
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=NAMA_SERVER\SQLEXPRESS
DB_NAME=project_db
DB_TRUSTED_CONNECTION=yes
```

### 4. Siapkan database SQL Server

Buat database `project_db` dan tiga tabel berikut:

```sql
CREATE TABLE mahasiswa (
    NIM BIGINT PRIMARY KEY,
    [NAMA LENGKAP] NVARCHAR(100),
    [KODE KELAS] NVARCHAR(20)
);

CREATE TABLE mata_kuliah (
    id_mk INT PRIMARY KEY,
    nama_mk NVARCHAR(100),
    sks INT
);

CREATE TABLE nilai (
    id_nilai INT IDENTITY PRIMARY KEY,
    nim BIGINT REFERENCES mahasiswa(NIM),
    id_mk INT,
    nilai FLOAT
);
```

### 5. (Opsional) Generate dan import data dummy

Jalankan script secara berurutan:

```bash
# 1. Generate file Excel berisi 1 juta data mahasiswa
python scripts/dummymahasiswa.py

# 2. Import data Excel ke SQL Server
python scripts/import_data_excel.py

# 3. Generate 10 juta data nilai
python scripts/dummynilai.py

# 4. Generate data mata kuliah
python scripts/dummymatakuliah.py
```

### 6. Jalankan server

```bash
uvicorn main:app --reload
```

API tersedia di `http://localhost:8000`. Dokumentasi interaktif di `http://localhost:8000/docs`.

## Endpoint API

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/add_data` | Tambah data mahasiswa, mata kuliah, dan nilai |
| GET | `/data_mahasiswa_nilai_mk/{nim}` | Ambil data lengkap berdasarkan NIM |
| PUT | `/update_data/{nim}` | Perbarui data berdasarkan NIM |
| DELETE | `/delete_data/{nim}` | Hapus data berdasarkan NIM |

## Teknologi

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [pyodbc](https://github.com/mkleehammer/pyodbc)
- [pandas](https://pandas.pydata.org/)
- [uvicorn](https://www.uvicorn.org/)
