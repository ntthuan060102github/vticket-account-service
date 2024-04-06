from django.urls import path

from vticket_app.views.token_pair_view import TokenPairView
from vticket_app.views.custom_refresh_token_view import CustomRefreshTokenView


urls = (
   path('token', TokenPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh', CustomRefreshTokenView.as_view(), name='token_refresh'),
)