from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.request import Request

from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.page_pagination import PagePagination
from vticket_app.services.user_service import UserService
from vticket_app.serializers.user_serializer import UserSerializer
from vticket_app.utils.response import RestResponse
from vticket_app.middlewares.custom_permissions.is_admin import IsAdmin
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.validations.get_users_validator import GetUsersValidation

class UserView(viewsets.ViewSet):
    permission_classes = (IsAdmin,)
    user_service = UserService()
    user_serializer = UserSerializer()

    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def retrieve(self, request: Request, pk=None):
        try:
            data = self.user_service.get_user_by_id(user_id=pk)

            if data is None:
                return RestResponse().defined_error().set_message("Không tìm thấy người dùng này trong hệ thống!").response 
            else:
                return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
    
    @action(methods=["GET"], detail=True, url_path="internal", authentication_classes=(), permission_classes=())
    def get_user_by_id(self, request: Request, pk=None):
        try:
            data = self.user_service.get_user_by_id(user_id=pk)

            if data is None:
                return RestResponse().defined_error().set_message("Không tìm thấy người dùng này trong hệ thống!").response 
            else:
                return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response

    @action(methods=["GET"], detail=True, url_path="lock")
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def lock_user(self, request: Request, pk=None):   
        try:
            result = self.user_service.lock_user(user_id=pk)

            return {
                1: RestResponse().defined_error().set_message("Tài khoản này đã bị khóa rồi!").response,
                2: RestResponse().success().set_message("Khóa tài khoản thành công!!").response,
                3: RestResponse().defined_error().set_message("Có chút trục trặc trong khi chúng tôi đang cố gắng thay đổi thông tin của bạn!").response
            }[result]
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["GET"], detail=True, url_path="unlock")
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
    @swagger_auto_schema(
        manual_parameters=[
            SwaggerProvider.header_authentication(),
            SwaggerProvider.query_param("kw", openapi.TYPE_STRING)
        ]
    )
    def search(self, request: Request):
        try:
            keyword = request.query_params.get("kw", None)
            data = self.user_service.search(keyword=keyword)

            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        

    @action(methods=["POST"], detail=False, url_path="list", authentication_classes=(), permission_classes=())
    @swagger_auto_schema(request_body=GetUsersValidation)
    @validate_body(GetUsersValidation)
    def get_user_by_ids(self, request: Request, validated_body):
        try:
            data = self.user_service.get_user_by_ids(ids=validated_body["ids"])
            return RestResponse().success().set_data(UserSerializer(data, many=True, fields={'id', 'first_name', 'last_name','avatar_url'}).data).response
                
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @swagger_auto_schema(
        manual_parameters=[
            SwaggerProvider.header_authentication(),
            SwaggerProvider.query_param("page_num", openapi.TYPE_INTEGER),
            SwaggerProvider.query_param("page_size", openapi.TYPE_INTEGER)
        ]
    )
    def list(self, request: Request):
        try:
            data = self.user_service.all()
            paginator = PagePagination()
            paginated_queryset = paginator.paginate_queryset(data, request)
            serialized_data = UserSerializer(paginated_queryset, many=True, exclude=["password"]).data
            return RestResponse().success().set_data(
                {
                'total_pages': paginator.page.paginator.num_pages,
                'total_items': paginator.page.paginator.count,
                'page_size': paginator.page.paginator.per_page,
                'data': serialized_data
                }
            ).response
        
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response