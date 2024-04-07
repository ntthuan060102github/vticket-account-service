from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from vticket_app.models.user import User
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.enums.account_error_enum import AccountErrorEnum
from vticket_app.helpers.regex_provider import RegexProvider
from vticket_app.services.account_service import AccountService
from vticket_app.validations.email_validator import EmailValidation
from vticket_app.validations.register_input_validator import RegisterInputValidator
from vticket_app.validations.email_and_otp_validator import EmailOTPValidation

class AccountView(viewsets.ViewSet):
    account_service = AccountService()
    regex_provider = RegexProvider()

    @action(methods=["POST"], detail=False, url_path="register")
    @swagger_auto_schema(request_body=RegisterInputValidator)
    @validate_body(RegisterInputValidator)
    def create_account(self, request: Request, validated_body: dict):
        try:
            self.account_service.create_account(User(**validated_body))
            
            return RestResponse().success().set_message("Chúc mừng! Bạn vừa tạo ra một hồn ma mới trong hệ thống!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["POST"], detail=False, url_path=f"verification")
    @swagger_auto_schema(request_body=EmailOTPValidation)
    @validate_body(EmailOTPValidation)
    def verify_account(self, request: Request, validated_data: dict):
        try:
            _email = validated_data["email"]
            _reset_result = self.account_service.verify_account(
                email=_email, 
                otp=validated_data["otp"]
            )

            return {
                AccountErrorEnum.ALL_OK: RestResponse().success().set_message("Tài khoản của bạn đã được xác minh thành công!").response,
                AccountErrorEnum.NOT_EXISTS: RestResponse().defined_error().set_message("Này bạn! Email mà bạn nhập không tồn tại trong hệ thống của chúng tôi.").response,
                AccountErrorEnum.INVALID_OTP: RestResponse().defined_error().set_message("OTP không hợp lệ hoặc đã hết hạn!").response
            }[_reset_result]
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["POST"], detail=False, url_path=f"reset-password/request")
    @swagger_auto_schema(request_body=EmailValidation)
    @validate_body(EmailValidation)
    def request_reset_password(self, request: Request, validated_data: dict):
        try:
            _email = validated_data["email"]
            _request_result = self.account_service.request_reset_password(_email)

            return {
                AccountErrorEnum.NOT_EXISTS: RestResponse().defined_error().set_message("Này bạn! Email mà bạn nhập không tồn tại trong hệ thống của chúng tôi.").response,
                AccountErrorEnum.ALL_OK: RestResponse().success().set_message(f"Vui lòng sử dụng OTP đã được gửi tới địa chỉ {_email} để khôi phục mật khẩu!").response,
            }[_request_result]
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["POST"], detail=False, url_path="reset-password")
    @swagger_auto_schema(request_body=EmailOTPValidation)
    @validate_body(EmailOTPValidation)
    def reset_password(self, request: Request, validated_data: dict):
        try:
            _email = validated_data["email"]
            _reset_result = self.account_service.reset_password(
                email=_email, 
                otp=validated_data["otp"]
            )

            return {
                AccountErrorEnum.ALL_OK: RestResponse().success().set_message(f"Vui lòng sử dụng mật khẩu đã được gửi tới địa chỉ {_email} để đăng nhập tài khoản!").response,
                AccountErrorEnum.NOT_EXISTS: RestResponse().defined_error().set_message("Này bạn! Email mà bạn nhập không tồn tại trong hệ thống của chúng tôi.").response,
                AccountErrorEnum.INVALID_OTP: RestResponse().defined_error().set_message("OTP không hợp lệ hoặc đã hết hạn!").response
            }[_reset_result]
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response