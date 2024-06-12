from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from vticket_app.models.user import User
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.services.account_service import AccountService
from vticket_app.enums.account_error_enum import AccountErrorEnum
from vticket_app.middlewares.custom_jwt_authentication import CustomJWTAuthentication

from vticket_app.helpers.regex_provider import RegexProvider
from vticket_app.helpers.swagger_provider import SwaggerProvider

from vticket_app.validations.email_validator import EmailValidation
from vticket_app.validations.email_and_otp_validator import EmailOTPValidation
from vticket_app.validations.register_input_validator import RegisterInputValidator
from vticket_app.validations.change_password_validator import ChangePasswordValidator

class AccountView(viewsets.ViewSet):
    account_service = AccountService()
    regex_provider = RegexProvider()
    authentication_classes = ()

    @action(methods=["POST"], detail=False, url_path="register")
    @swagger_auto_schema(request_body=RegisterInputValidator)
    @validate_body(RegisterInputValidator)
    def create_account(self, request: Request, validated_body: dict):
        try:
            result = self.account_service.create_account(User(**validated_body))
            _email = validated_body["email"]

            return {
                AccountErrorEnum.ALL_OK: RestResponse().direct(f"/otp/{_email}").set_message("Chúc mừng! Bạn vừa tạo ra một hồn ma mới trong hệ thống!").response,
                AccountErrorEnum.EXISTED: RestResponse().defined_error().set_message("Email đã tồn tại trong hệ thống!").response,
            }[result]
            
            return 
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
        
    @action(methods=["POST"], detail=False, url_path="change-password", authentication_classes=(CustomJWTAuthentication,))
    @swagger_auto_schema(request_body=ChangePasswordValidator, manual_parameters=[SwaggerProvider.header_authentication()])
    @validate_body(ChangePasswordValidator)
    def change_password(self, request: Request, validated_data: dict):
        try:
            result = self.account_service.change_password(
                user_id=request.user.id,
                old_password=validated_data["old_password"],
                new_password=validated_data["new_password"]
            )

            return {
                AccountErrorEnum.INCORRECT_PASSWORD: RestResponse().defined_error().set_message("Mật khẩu hiện tại chưa chính xác!").response,
                AccountErrorEnum.WEAK_PASSWORD: RestResponse().defined_error().set_message("Mẩt khẩu phải dài tối thiểu 8 ký tực và tối đa 30 ký tự, bao gồm ít nhất một chữ thường, một chữ hoa, một chữ số và một ký tự đặc biệt!").response,
                AccountErrorEnum.NOT_EXISTS: RestResponse().defined_error().set_message("Này bạn! Tài khoản của bạn không tồn tại trong hệ thống của chúng tôi.").response,
                AccountErrorEnum.ALL_OK: RestResponse().success().set_message("Great job! Mật khẩu mới của bạn đã được cập nhật thành công. Bạn đã làm một việc tuyệt vời để bảo vệ thông tin cá nhân của mình!").response,
            }[result]
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response