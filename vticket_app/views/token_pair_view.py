from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView

from vticket_app.errors.un_verified_exception import UnVerifiedException
from vticket_app.services.account_service import AccountService
from vticket_app.services.profile_service import ProfileService
from vticket_app.utils.response import RestResponse

class TokenPairView(TokenObtainPairView):
    account_service = AccountService()
    profile_service = ProfileService()
    
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            print()
        
            return RestResponse().success().set_data(
                {
                    **response.data,
                    "profile": self.profile_service.get_profile_by_email(request.data["email"])
                }
            ).response
        except serializers.ValidationError:
            return RestResponse().validation_failed().set_message("Dữ liệu đầu vào không hợp lệ!").response
        except UnVerifiedException as e:
            _email = request.data["email"]
            self.account_service.resend_registration_otp(_email)
            return RestResponse().direct(f"/otp/{_email}").response
        except exceptions.AuthenticationFailed as e:
            return RestResponse().defined_error().set_message("Thông tin tài khoản không chính xác!").response
        except exceptions.PermissionDenied as e:
            return RestResponse().defined_error().set_message("Tài khoản đã bị khóa!").response
        