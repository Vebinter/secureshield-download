#!/usr/bin/env python3
"""Защита от модификации: контрольные суммы всех файлов"""
import hashlib, os, json

PROG_DIR = "/opt/secureshield"
HASH_FILE = "/etc/secureshield/integrity.json"

def calc_hashes():
    hashes = {}
    for root, dirs, files in os.walk(PROG_DIR):
        for f in files:
            if f.endswith(('.py', '.sh', '.json')):
                path = os.path.join(root, f)
                with open(path, 'rb') as fh:
                    hashes[path] = hashlib.sha256(fh.read()).hexdigest()
    return hashes

def save_integrity():
    hashes = calc_hashes()
    os.makedirs("/etc/secureshield", exist_ok=True)
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)
    print(f"✅ Контрольные суммы сохранены: {len(hashes)} файлов")

def verify_integrity():
    if not os.path.exists(HASH_FILE):
        print("⚠️ Нет файла целостности — создаём")
        save_integrity()
        return True
    with open(HASH_FILE) as f:
        saved = json.load(f)
    current = calc_hashes()
    modified = []
    for path, h in saved.items():
        if path not in current or current[path] != h:
            modified.append(path)
    if modified:
        print(f"⚠️ МОДИФИЦИРОВАНО {len(modified)} файлов:")
        for m in modified: print(f"   ❌ {m}")
        return False
    print(f"✅ Все {len(saved)} файлов целы! Модификация не обнаружена.")
    return True

if __name__ == "__main__":
    print("🔒 SecureShield Integrity Check")
    save_integrity()
    verify_integrity()
