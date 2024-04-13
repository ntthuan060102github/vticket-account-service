from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView

from vticket_app.errors.un_verified_exception import UnVerifiedException
from vticket_app.utils.response import RestResponse

class TokenPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        
            return RestResponse().success().set_data(response.data).response
        except serializers.ValidationError:
            return RestResponse().validation_failed().set_message("Dữ liệu đầu vào không hợp lệ!").response
        except UnVerifiedException as e:
            _email = request.data["email"]
            return RestResponse().direct(f"/otp/{_email}").response
        except exceptions.AuthenticationFailed as e:
            return RestResponse().defined_error().set_message("Thông tin tài khoản không chính xác!").response
        except exceptions.PermissionDenied as e:
            return RestResponse().defined_error().set_message("Tài khoản đã bị khóa!").response
        