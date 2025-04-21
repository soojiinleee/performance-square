from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserSignupView

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_register"),  # 회원가입
    path(
        "signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # 로그인 (JWT 발급)
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # JWT 갱신
]
