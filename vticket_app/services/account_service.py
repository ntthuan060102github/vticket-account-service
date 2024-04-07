from django.core.exceptions import ObjectDoesNotExist

from vticket_app.helpers.otp_provider import OTPProvider
from vticket_app.models.user import User
from vticket_app.enums.account_error_enum import AccountErrorEnum
from vticket_app.enums.account_status_enum import AccountStatusEnum
from vticket_app.helpers.password_provider import PasswordProvider
from vticket_app.helpers.email_providers.email_provider import EmailProvider

class AccountService():
    email_provider = EmailProvider()
    password_provider = PasswordProvider()
    otp_provider = OTPProvider()
    mail_info = {
        "registration": ("otp_register_mail.html", "[V-Ticket] OTP Verification"),
        "reset_password": ("otp_reset_password_mail.html", "[V-Ticket] OTP Verification"),
        "new_password": ("reset_password_mail.html", "[V-Ticket] New your password")
    }

    def create_account(self, account : User) -> None:
        try:
            account.set_password(account.password)
            account.status = AccountStatusEnum.UNVERIFIED
            account.save()
            
            otp = self.otp_provider.generate_6_char()
            self.otp_provider.save_otp_to_time_db(otp=otp, key=f"registration:{account.email}", ttl=15*60)
            
            return self.email_provider.send_html_template_email(
                to=[account.email],
                cc=[],
                subject=self.mail_info["registration"][1],
                template_name=self.mail_info["registration"][0],
                context={
                    "otp": otp
                }
            )
        except Exception as e:
            print(e)
            raise Exception(e)
        
    def request_reset_password(self, email: str) -> AccountErrorEnum:
        try:
            account = User.objects.get(email=email)
            otp = self.otp_provider.generate_6_char()
            self.otp_provider.save_otp_to_time_db(otp=otp, key=f"reset_password:{email}", ttl=15*60)

            self.email_provider.send_html_template_email(
                to=[account.email],
                cc=[],
                subject=self.mail_info["reset_password"][1],
                template_name=self.mail_info["reset_password"][0],
                context={
                    "otp": otp
                }
            )
            
            return AccountErrorEnum.ALL_OK
        except ObjectDoesNotExist:
            return AccountErrorEnum.NOT_EXISTS
        except Exception as e:
            print(e)
            raise e
        
    def reset_password(self, email: str, otp: str) -> AccountErrorEnum:
        try:
            account = User.objects.get(email=email)

            if not self.otp_provider.verify_otp(otp=otp, key=f"reset_password:{email}", delete=True):
                return AccountErrorEnum.INVALID_OTP

            new_password = self.password_provider.generate_strong_password()
            account.set_password(new_password)
            account.save(update_fields=["password"])

            self.email_provider.send_html_template_email(
                to=[account.email],
                cc=[],
                subject=self.mail_info["new_password"][1],
                template_name=self.mail_info["new_password"][0],
                context={
                    "new_password": new_password
                }
            )
            return AccountErrorEnum.ALL_OK
        except ObjectDoesNotExist:
            return AccountErrorEnum.NOT_EXISTS
        except Exception as e:
            print(e)
            raise e
        
    def verify_account(self, email: str, otp: str):
        try:
            account = User.objects.get(email=email)

            if not self.otp_provider.verify_otp(otp=otp, key=f"registration:{email}", delete=True):
                return AccountErrorEnum.INVALID_OTP
            
            account.status = AccountStatusEnum.ACTIVED
            account.save(update_fields=["status"])

            return AccountErrorEnum.ALL_OK
        except ObjectDoesNotExist:
            return AccountErrorEnum.NOT_EXISTS
        except Exception as e:
            print(e)
            raise e
        
    def change_password(self, user_id: int, old_password: str, new_password: str) -> AccountErrorEnum:
        try:
            account = User.objects.get(id=user_id)

            if not account.check_password(old_password):
                return AccountErrorEnum.INCORRECT_PASSWORD
            
            if not self.password_provider.check_password_strength(new_password):
                return AccountErrorEnum.WEAK_PASSWORD
            
            account.set_password(new_password)
            account.save(update_fields=["password"])
            
            return AccountErrorEnum.ALL_OK
        except ObjectDoesNotExist:
            return AccountErrorEnum.NOT_EXISTS
        except Exception as e:
            print(e)
            raise e