import pandas as pd
import random

# Daftar nama depan dan nama belakang yang umum
first_names = [
    "Michael", "Ethan", "William", "Ava", "James", "Alex", "Chris", "Sophia", "Sarah",
    "Olivia", "John", "Daniel", "Jane", "David", "Katie", "Emily", "Isabella", "Andrew", "Laura", "Emma"
]

last_names = [
    "Garcia", "Jackson", "Thomas", "Davis", "Rodriguez", "Anderson", "Brown",
    "Hernandez", "Gonzalez", "Smith", "Taylor", "Jones", "Miller", "Williams",
    "Martin", "Johnson", "Wilson", "Lopez", "Martinez", "Moore"
]

# Fungsi untuk menghasilkan nama lengkap
def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Generate data
nim_start = 20240000001
nim_end = 20241000000
nim_list = list(range(nim_start, nim_start + 1000000))  # Membuat NIM dari 20240000001 hingga 20241000000 (1 juta data)

# Kode kelas dari LIE00001 hingga LIE25000
kode_kelas_list = [f"LIE{str(i).zfill(5)}" for i in range(1, 25001)]

# Membuat list nama acak
names_list = [generate_name() for _ in range(1000000)]

# Membuat list kode kelas sesuai dengan pembagian per-40 nim
kode_kelas_assignments = [kode_kelas_list[i // 40] for i in range(1000000)]

# Membuat DataFrame
df = pd.DataFrame({
    'NIM': nim_list,
    'Nama Lengkap': names_list,
    'Kode Kelas': kode_kelas_assignments
})

# Menyimpan DataFrame ke file Excel
output_file = "mahasiswa.xlsx"
df.to_excel(output_file, index=False)

print(f"File Excel '{output_file}' telah berhasil dibuat!")
