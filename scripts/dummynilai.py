"""
Script untuk generate 10 juta data dummy nilai ke SQL Server.
Jalankan setelah import_data_excel.py berhasil mengisi tabel mahasiswa.
"""
import pyodbc
import random
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

cursor.execute("SELECT NIM FROM mahasiswa")
nim_list = [row[0] for row in cursor.fetchall()]

data_dummy = []
num_records = 10000000  # 10 juta data
for id_mk in range(1, num_records + 1):
    nim = random.choice(nim_list)
    nilai = round(random.uniform(0, 100), 2)
    data_dummy.append((id_mk, nim, nilai))

insert_query = "INSERT INTO nilai (id_mk, nim, nilai) VALUES (?, ?, ?)"
cursor.executemany(insert_query, data_dummy)
conn.commit()

print("Data dummy nilai berhasil dimasukkan!")
cursor.close()
conn.close()
