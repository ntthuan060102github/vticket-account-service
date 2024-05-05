from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.request import Request

from vticket_app.dtos.user_dto import UserDTO
from vticket_app.services.user_service import UserService
from vticket_app.serializers.user_serializer import UserSerializer
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.serializers.update_profile_serializer import UpdateProfileSerializer
from vticket_app.middlewares.custom_permissions.is_admin import IsAdmin
from vticket_app.helpers.swagger_provider import SwaggerProvider

class UserView(viewsets.ViewSet):
    permission_classes = (IsAdmin,)
    user_service = UserService()
    user_serializer = UserSerializer()

    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def retrieve(self, request: Request, pk=None):
        try:
            data = self.user_service.get_user_by_id(user_id=pk)
            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response

    @action(methods=["PATCH"], detail=True, url_path="lock")
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def lock_user(self, request: Request, pk=None):   
        try:
            result = self.user_service.lock_user(user_id=pk)
            if result:
                return RestResponse().success().set_message("Khóa tài khoản thành công!!").response
            else:
                return RestResponse().defined_error().set_message("Có chút trục trặc trong khi chúng tôi đang cố gắng thay đổi thông tin của bạn!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["PATCH"], detail=True, url_path="unlock")
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def unlock_user(self, request: Request, pk=None):   
        try:
            result = self.user_service.unlock_user(user_id=pk)
            if result:
                return RestResponse().success().set_message("Mở khóa tài khoản thành công!!").response
            else:
                return RestResponse().defined_error().set_message("Có chút trục trặc trong khi chúng tôi đang cố gắng thay đổi thông tin của bạn!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["GET"], detail=False, url_path="search")
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def lock_user(self, request: Request):
        try:
            keyword = request.query_params.get("keyword")
            data = self.user_service.search(keyword=keyword)
            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response