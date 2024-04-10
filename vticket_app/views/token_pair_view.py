from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import exceptions

from vticket_app.utils.response import RestResponse

class TokenPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return RestResponse().success().set_data(response.data).response
        except exceptions.AuthenticationFailed as e:
            return RestResponse().defined_error().set_message("Thông tin tài khoản không chính xác!").response
        except exceptions.PermissionDenied as e:
            return RestResponse().defined_error().set_message("Tài khoản chưa được xác thực hoặc đã bị khóa!").response
        