import random
from typing import Any
from django.core.cache import cache

class OTPProvider():
    def generate_6_char(self) -> str:
        return str(random.randint(100000, 999999))
    
    def save_otp_to_time_db(self, otp:str, key: str, ttl: int = 15*60) -> None:
        cache.set(f"otp:{key}", otp, ttl)

    def verify_otp(self, otp: str, key:str, delete: bool = False) -> bool:
        is_valid = cache.get(key=f"otp:{key}", default=None)  == otp

        if delete:
            cache.delete(key=f"otp:{key}")

        return is_valid

    