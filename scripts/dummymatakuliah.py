"""
Script untuk generate data dummy mata kuliah ke SQL Server.
Jalankan setelah dummynilai.py berhasil dijalankan.
"""
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME", "project_db")
DB_TRUSTED = os.getenv("DB_TRUSTED_CONNECTION", "yes")

conn_str = (
    f"Driver={{{DB_DRIVER}}};"
    f"Server={DB_SERVER};"
    f"Database={DB_NAME};"
    f"Trusted_Connection={DB_TRUSTED};"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Daftar nama mata kuliah realistis
realistic_courses = [
    "Matematika Dasar", "Fisika", "Kimia", "Biologi", "Pemrograman Dasar",
    "Algoritma dan Struktur Data", "Basis Data", "Jaringan Komputer",
    "Sistem Operasi", "Kecerdasan Buatan", "Etika Profesi", "Manajemen Proyek",
    "Pemrograman Berbasis Objek", "Analisis Data", "Desain Antarmuka Pengguna",
    "Pengolahan Sinyal Digital", "Komputasi Awan", "Pemrograman Mobile",
    "Keamanan Siber", "Kalkulus Lanjutan"
]

cursor.execute("SELECT DISTINCT id_mk FROM nilai")
id_mk_list = cursor.fetchall()

dummy_mata_kuliah = []
for i, id_mk in enumerate(id_mk_list):
    nama_mk = realistic_courses[i % len(realistic_courses)]
    sks = (i % 4) + 2  # SKS antara 2-5
    dummy_mata_kuliah.append((id_mk[0], nama_mk, sks))

insert_query = "INSERT INTO mata_kuliah (id_mk, nama_mk, sks) VALUES (?, ?, ?)"
cursor.executemany(insert_query, dummy_mata_kuliah)
conn.commit()
print("Data dummy mata kuliah berhasil dimasukkan.")

alter_query = """
ALTER TABLE nilai
ADD CONSTRAINT FK_nilai_mata_kuliah
FOREIGN KEY (id_mk) REFERENCES mata_kuliah(id_mk);
"""
cursor.execute(alter_query)
conn.commit()
print("Foreign key antara tabel nilai dan mata_kuliah berhasil dibuat.")

cursor.close()
conn.close()
