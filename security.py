# // Security.py
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

load_dotenv()
RAW_KEY = os.getenv("ENCRYPTION_KEY")

if not RAW_KEY:
    print("ENCRYPTION_KEY, Bulunamadı oluşturuluyor...")
    RAW_KEY = Fernet.generate_key().decode()
    with open(".env", "a",) as f:
        f.write(f"\nENCRYPTION_KEY={RAW_KEY}\n")

cipher = Fernet(RAW_KEY.encode() if isinstance(RAW_KEY, str) else RAW_KEY)

def encrypt_api_key(api_key: str) -> str:
    return cipher.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str) -> str:
    return cipher.decrypt(encrypted_key.encode()).decode()