import string
import secrets

class PasswordProvider():
    STRONG_LENGTH = 20 

    def generate_strong_password(self) -> str:
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for i in range(self.STRONG_LENGTH))
        return password