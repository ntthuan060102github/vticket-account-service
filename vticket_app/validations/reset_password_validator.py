from rest_framework import serializers

from vticket_app.validations.email_validator import EmailValidation

class ResetPasswordValidation(EmailValidation):
    otp = serializers.CharField(required=True, allow_blank=False)