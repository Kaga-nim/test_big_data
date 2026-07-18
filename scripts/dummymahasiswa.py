"""
Script untuk generate data dummy mahasiswa ke file Excel.
Jalankan sekali untuk membuat mahasiswa.xlsx sebelum import ke database.
"""
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

def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Generate data
nim_start = 20240000001
nim_list = list(range(nim_start, nim_start + 1000000))  # 1 juta data

# Kode kelas dari LIE00001 hingga LIE25000
kode_kelas_list = [f"LIE{str(i).zfill(5)}" for i in range(1, 25001)]

names_list = [generate_name() for _ in range(1000000)]
kode_kelas_assignments = [kode_kelas_list[i // 40] for i in range(1000000)]

df = pd.DataFrame({
    'NIM': nim_list,
    'Nama Lengkap': names_list,
    'Kode Kelas': kode_kelas_assignments
})

output_file = "mahasiswa.xlsx"
df.to_excel(output_file, index=False)
print(f"File Excel '{output_file}' berhasil dibuat!")
