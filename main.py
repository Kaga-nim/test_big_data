from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Koneksi ke SQL Server (konfigurasi dari file .env)
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

# Nama file Excel
EXCEL_FILE = "mahasiswa.xlsx"

# Model data untuk input
class DataInput(BaseModel):
    nim: str
    nama_lengkap: str
    kode_kelas: str
    id_nilai: int
    id_mk: int
    nilai: float
    nama_mk: str
    sks: int

# Fungsi untuk memuat data dari Excel
def load_excel():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=["NIM", "Nama Lengkap", "Kode Kelas"])

# Fungsi untuk menyimpan data ke Excel
def save_to_excel(df):
    df.to_excel(EXCEL_FILE, index=False)

# CREATE
@app.post("/add_data")
def add_data(data: DataInput):
    try:
        # Tambahkan data ke tabel mahasiswa
        insert_mahasiswa_query = """
        INSERT INTO mahasiswa (NIM, [NAMA LENGKAP], [KODE KELAS])
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_mahasiswa_query, data.nim, data.nama_lengkap, data.kode_kelas)

        # Tambahkan data ke tabel mata_kuliah
        insert_mata_kuliah_query = """
        INSERT INTO mata_kuliah (id_mk, nama_mk, sks)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_mata_kuliah_query, data.id_mk, data.nama_mk, data.sks)

        # Tambahkan data ke tabel nilai
        insert_nilai_query = """
        INSERT INTO nilai (nim, id_mk, nilai)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_nilai_query, data.nim, data.id_mk, data.nilai)

        # Commit perubahan ke database
        conn.commit()

        # Tambahkan data ke Excel
        df = load_excel()
        if data.nim in df["NIM"].values:
            raise HTTPException(status_code=400, detail="NIM sudah ada di Excel.")

        new_row = {"NIM": data.nim, "Nama Lengkap": data.nama_lengkap, "Kode Kelas": data.kode_kelas}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_to_excel(df)

        return {"message": "Data berhasil ditambahkan."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# READ
@app.get("/data_mahasiswa_nilai_mk/{nim}")
def get_data_mahasiswa_nilai_mk(nim: str):
    query = """
    SELECT 
        m.NIM,
        m.[NAMA LENGKAP],
        m.[KODE KELAS],
        n.id_nilai,
        n.id_mk,
        n.nilai,
        mk.nama_mk,
        mk.sks
    FROM mahasiswa m
    JOIN nilai n ON m.NIM = n.nim
    JOIN mata_kuliah mk ON n.id_mk = mk.id_mk
    WHERE m.NIM = ?
    """
    cursor.execute(query, nim)
    rows = cursor.fetchall()

    if rows:
        result = [
            {
                "nim": row[0],
                "nama_lengkap": row[1],
                "kode_kelas": row[2],
                "id_nilai": row[3],
                "id_mk": row[4],
                "nilai": row[5],
                "nama_mk": row[6],
                "sks": row[7]
            }
            for row in rows
        ]
        return result
    else:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")

# UPDATE
@app.put("/update_data/{nim}")
def update_data(nim: str, data: DataInput):
    try:
        # Perbarui data di tabel mahasiswa
        update_mahasiswa_query = """
        UPDATE mahasiswa
        SET [NAMA LENGKAP] = ?, [KODE KELAS] = ?
        WHERE NIM = ?
        """
        cursor.execute(update_mahasiswa_query, data.nama_lengkap, data.kode_kelas, nim)

        # Perbarui data di tabel mata_kuliah
        update_mata_kuliah_query = """
        UPDATE mata_kuliah
        SET nama_mk = ?, sks = ?
        WHERE id_mk = ?
        """
        cursor.execute(update_mata_kuliah_query, data.nama_mk, data.sks, data.id_mk)

        # Perbarui data di tabel nilai
        update_nilai_query = """
        UPDATE nilai
        SET nilai = ?
        WHERE nim = ? AND id_mk = ?
        """
        cursor.execute(update_nilai_query, data.nilai, nim, data.id_mk)

        # Commit perubahan ke database
        conn.commit()

        # Perbarui data di Excel
        df = load_excel()
        if nim not in df["NIM"].values:
            raise HTTPException(status_code=404, detail="Data tidak ditemukan di Excel.")

        df.loc[df["NIM"] == nim, ["Nama Lengkap", "Kode Kelas"]] = [data.nama_lengkap, data.kode_kelas]
        save_to_excel(df)

        return {"message": "Data berhasil diperbarui."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# DELETE
@app.delete("/delete_data/{nim}")
def delete_data(nim: str):
    try:
        # Hapus data dari tabel nilai
        delete_nilai_query = "DELETE FROM nilai WHERE nim = ?"
        cursor.execute(delete_nilai_query, nim)

        # Hapus data dari tabel mahasiswa
        delete_mahasiswa_query = "DELETE FROM mahasiswa WHERE NIM = ?"
        cursor.execute(delete_mahasiswa_query, nim)

        # Commit perubahan ke database
        conn.commit()

        # Hapus data di Excel
        df = load_excel()
        if nim not in df["NIM"].values:
            raise HTTPException(status_code=404, detail="Data tidak ditemukan di Excel.")

        df = df[df["NIM"] != nim]
        save_to_excel(df)

        return {"message": "Data berhasil dihapus."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
