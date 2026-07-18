import pyodbc
import random

# Koneksi ke SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=KAGA-NIM\\SQLEXPRESS;"  # Ganti dengan nama server kamu
    "Database=project_db;"  # Nama database
    "Trusted_Connection=yes;"  # Untuk Windows Authentication
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Mengambil semua NIM dari tabel mahasiswa
cursor.execute("SELECT NIM FROM mahasiswa")
nim_list = [row[0] for row in cursor.fetchall()]

# Membuat data dummy dengan id_mk unik
data_dummy = []
num_records = 10000000  # 10 juta data
for id_mk in range(1, num_records + 1):  # Pastikan id_mk unik
    nim = random.choice(nim_list)  # Pilih NIM secara acak
    nilai = round(random.uniform(0, 100), 2)  # Nilai antara 0 dan 100

    data_dummy.append((id_mk, nim, nilai))

# Insert data dummy ke tabel nilai
insert_query = """
INSERT INTO nilai (id_mk, nim, nilai)
VALUES (?, ?, ?)
"""
cursor.executemany(insert_query, data_dummy)
conn.commit()

print("Data dummy berhasil dimasukkan!")
