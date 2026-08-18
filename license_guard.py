#!/usr/bin/env python3
"""SecureShield License Guard v2.0 — Невозможно взломать"""
import hashlib, hmac, uuid, subprocess, os, json
from datetime import datetime

class LicenseGuard:
    SECRET_SALT = "SS2026_OlegBelyaev_NE_VZLOMAESH"
    
    def get_hardware_id(self):
        mac = uuid.getnode()
        try:
            cpu = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | head -1", shell=True).decode().strip()
        except: cpu = "unknown"
        raw = f"{mac}:{cpu}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    
    def generate_key(self):
        hw_id = self.get_hardware_id()
        timestamp = datetime.now().strftime("%Y%m%d")
        raw = f"{self.SECRET_SALT}:{hw_id}:{timestamp}"
        h1 = hashlib.sha512(raw.encode()).hexdigest()
        h2 = hmac.new(self.SECRET_SALT.encode(), h1.encode(), hashlib.sha256).hexdigest()
        h3 = hashlib.sha256(h2.encode()).hexdigest()[:32].upper()
        return f"SS-{h3[:8]}-{h3[8:16]}-{h3[16:24]}-{h3[24:32]}"
    
    def verify_key(self, input_key):
        return hmac.compare_digest(input_key, self.generate_key())
    
    def save_license(self):
        key = self.generate_key()
        hw_id = self.get_hardware_id()
        data = {"key": key, "hw_id": hw_id, "created": datetime.now().isoformat(),
                "checksum": hashlib.sha256(f"{key}:{hw_id}:{self.SECRET_SALT}".encode()).hexdigest()}
        os.makedirs("/etc/secureshield", exist_ok=True)
        with open("/etc/secureshield/license.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Ключ: {key}")
        print(f"✅ Hardware: {hw_id}")
        return key
    
    def check_integrity(self):
        try:
            with open("/etc/secureshield/license.json") as f:
                data = json.load(f)
            expected = hashlib.sha256(f"{data['key']}:{data['hw_id']}:{self.SECRET_SALT}".encode()).hexdigest()
            return data.get("checksum") == expected and self.verify_key(data["key"])
        except: return False

if __name__ == "__main__":
    g = LicenseGuard()
    print("🔒 SecureShield License Guard v2.0")
    print(f"📊 Hardware ID: {g.get_hardware_id()}")
    g.save_license()
    print(f"🔐 Проверка: {'✅ ОК' if g.check_integrity() else '❌ ОШИБКА'}")
