import pyodbc

# Koneksi ke SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=KAGA-NIM\\SQLEXPRESS;"
    "Database=project_db;"
    "Trusted_Connection=yes;"
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

# Mengambil semua id_mk dari tabel nilai
cursor.execute("SELECT DISTINCT id_mk FROM nilai")
id_mk_list = cursor.fetchall()

# Membuat data dummy untuk mata kuliah
dummy_mata_kuliah = []
for i, id_mk in enumerate(id_mk_list):
    nama_mk = realistic_courses[i % len(realistic_courses)]  # Siklus nama jika data lebih banyak
    sks = (i % 4) + 2  # SKS bervariasi antara 2 hingga 5
    dummy_mata_kuliah.append((id_mk[0], nama_mk, sks))

# Memasukkan data dummy ke tabel mata_kuliah
insert_query = "INSERT INTO mata_kuliah (id_mk, nama_mk, sks) VALUES (?, ?, ?)"
cursor.executemany(insert_query, dummy_mata_kuliah)
conn.commit()
print("Data dummy berhasil dimasukkan ke tabel mata_kuliah.")

# Menambahkan foreign key antara tabel nilai dan tabel mata_kuliah
alter_query = """
ALTER TABLE nilai
ADD CONSTRAINT FK_nilai_mata_kuliah
FOREIGN KEY (id_mk) REFERENCES mata_kuliah(id_mk);
"""
cursor.execute(alter_query)
conn.commit()
print("Foreign key antara tabel nilai dan mata_kuliah berhasil dibuat.")

# Tutup koneksi
cursor.close()
conn.close()
