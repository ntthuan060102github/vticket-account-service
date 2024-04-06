from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenRefreshView

from vticket_app.utils.response import RestResponse

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            return RestResponse().defined_error().set_message("Refresh token hết hạn hoặc không hợp lệ!").response
        return RestResponse().success().set_data(response.data).response