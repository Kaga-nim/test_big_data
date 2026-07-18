"""
Script untuk mengimpor data mahasiswa dari mahasiswa.xlsx ke SQL Server.
Jalankan setelah dummymahasiswa.py berhasil membuat file Excel.
"""
import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME", "project_db")
DB_TRUSTED = os.getenv("DB_TRUSTED_CONNECTION", "yes")

connection_string = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"Trusted_Connection={DB_TRUSTED};"
)

file_path = "mahasiswa.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO mahasiswa (NIM, [NAMA LENGKAP], [KODE KELAS])
            VALUES (?, ?, ?)
        """, row["NIM"], row["NAMA LENGKAP"], row["KODE KELAS"])
    except pyodbc.IntegrityError:
        print(f"Data dengan NIM {row['NIM']} sudah ada, dilewati.")
    except Exception as e:
        print(f"Error pada baris {index}: {e}")

conn.commit()
cursor.close()
conn.close()
print("Data berhasil diimpor ke SQL Server!")
