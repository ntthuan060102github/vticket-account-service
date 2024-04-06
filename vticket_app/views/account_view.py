from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from vticket_app.decorators.validate_body import validate_body
from vticket_app.models.user import User
from vticket_app.services.account_service import AccountService
from vticket_app.validations.register_input_validator import RegisterInputValidator
from vticket_app.utils.response import RestResponse

class AccountView(viewsets.ViewSet):
    account_service = AccountService()

    @action(methods=["POST"], detail=False, url_path="register")
    @swagger_auto_schema(request_body=RegisterInputValidator)
    @validate_body(RegisterInputValidator)
    def create_account(self, request, validated_body):
        try:
            self.account_service.create_account(User(**validated_body))
            
            return RestResponse().success().set_message("Chúc mừng! Bạn vừa tạo ra một hồn ma mới trong hệ thống!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response