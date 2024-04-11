from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.request import Request

from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.services.profile_service import ProfileService
from vticket_app.validations.change_avatar_validator import ChangeAvatarValidator

from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.helpers.image_storage_providers.image_storage_provider import ImageStorageProvider
from vticket_app.helpers.image_storage_providers.firebase_storage_provider import FirebaseStorageProvider

class ProfileView(viewsets.ViewSet):
    image_storage_provider: ImageStorageProvider = FirebaseStorageProvider()
    profile_service = ProfileService()

    @action(methods=["POST"], detail=False, url_path="avatar", parser_classes=[MultiPartParser])
    @swagger_auto_schema(
        request_body=None,
        manual_parameters=[
            SwaggerProvider.header_authentication(),
            SwaggerProvider.form_data("image", openapi.TYPE_FILE)
        ]
    )
    @validate_body(ChangeAvatarValidator)
    def change_avatar(self, request: Request, validated_body):
        try:
            url = self.image_storage_provider.upload_image(validated_body["image"])
            updated = self.profile_service.change_avatar(request.user.id, url)
            if updated:
                return RestResponse().success().set_message("Một diện mạo mới, một tinh thần mới! 😄✨").response
            else:
                return RestResponse().defined_error().set_message("Có chút trục trặc trong khi chúng tôi đang cố gắng thay bức hình tuyệt vời này!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response