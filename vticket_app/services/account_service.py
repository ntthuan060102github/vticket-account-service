import random
from typing import Any
from django.core.cache import cache

from vticket_app.enums.account_status_enum import AccountStatusEnum
from vticket_app.models.user import User
from vticket_app.services.email_providers.email_provider import EmailProvider

class AccountService():
    email_provider = EmailProvider()
    templates = {
        "registration": "otp_register_mail.html",
        "forgot_password": "otp_forgot_password_mail.html"
    }

    def create_account(self, account : User) -> None:
        try:
            account.set_password(account.password)
            account.status = AccountStatusEnum.UNVERIFIED
            account.save()
            self.__send_otp(account, key="registration")
        except Exception as e:
            print(e)
            raise Exception(e)
        
    def __send_otp(self, user: User, key: str):
        otp = self.__generate_otp()
        self.__save_otp(otp=otp, key=key, value=user.email, ttl=15*60)
        return self.__send_otp_mail(otp=otp, email=user.email, key=key)
        
    def __generate_otp(self) -> str:
        return str(random.randint(100000, 999999))
    
    def __send_otp_mail(self, otp, email, key) -> int:
        return self.email_provider.send_html_template_email(
            [email],
            [],
            "[V-Ticket] OTP Verification",
            self.templates[key],
            {
                "otp": otp
            }
        )
    
    def __save_otp(self, otp: str, key: str, value: Any, ttl: int):
        cache.set(f"otp:{key}:{otp}", value, ttl)