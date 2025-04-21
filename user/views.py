from http.client import responses

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserTokenResponseSerializer


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response_data = UserTokenResponseSerializer(
            data={
                "access_token": access_token,
                "refresh_token": str(refresh),
            }
        )
        response_data.is_valid(raise_exception=True)

        return Response(response_data.data, status=status.HTTP_201_CREATED)
