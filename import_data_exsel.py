import pandas as pd
import pyodbc

# Konfigurasi koneksi ke SQL Server
server = 'KAGA-NIM\\SQLEXPRESS'
database = 'project_db'
username = 'your_username'  # Jika menggunakan autentikasi SQL Server
password = 'your_password'  # Jika menggunakan autentikasi SQL Server
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

# Baca data dari file Excel
file_path = 'mahasiswa.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Koneksi ke SQL Server
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Masukkan data ke tabel mahasiswa
for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO mahasiswa (NIM, [NAMA LENGKAP], [KODE KELAS])
            VALUES (?, ?, ?)
        """, row['NIM'], row['NAMA LENGKAP'], row['KODE KELAS'])
    except pyodbc.IntegrityError:
        print(f"Data with NIM {row['NIM']} already exists, skipping.")
    except Exception as e:
        print(f"Error inserting data at row {index}: {e}")

# Commit transaksi dan tutup koneksi
conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted!")

