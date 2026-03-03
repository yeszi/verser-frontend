# generate_hash.py
# Jalankan SEKALI SAJA di lokal untuk membuat hash password admin
# Perintah: python generate_hash.py
# Lalu copy output ke .env dan Vercel Environment Variables

from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,
    memory_cost=19456,  
    parallelism=1
)

password = input("anakrajin")
hashed = ph.hash(password)

print("\n✅ Hash berhasil dibuat!")
print("Salin baris berikut ke .env dan Vercel Environment Variables:\n")
print(f"ADMIN_PASSWORD_HASH={hashed}")