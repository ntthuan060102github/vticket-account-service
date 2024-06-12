import re
import string
import secrets

from vticket_app.helpers.regex_provider import RegexProvider

class PasswordProvider():
    RESETED_PASSWORD_LENGTH = 20
    password_8_30_uppercase_lowercase_number_special_char = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%_*?&-]{8,30}$"

    def generate_strong_password(self) -> str:
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for i in range(self.RESETED_PASSWORD_LENGTH))
        return password
    
    def check_password_strength(self, password):
        return bool(re.match(self.password_8_30_uppercase_lowercase_number_special_char, password))