import json
import bcrypt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import Account

from django.views import View
from django.http import JsonResponse

from login.serializers import LoginSerializer


class LoginView(View):
    def post(self, request):
        serializer = LoginSerializer(data=json.loads(request.body))
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            if Account.objects.filter(email=data["email"]).exists():
                user = Account.objects.get(email=data["email"])

                if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                    token = TokenObtainPairSerializer.get_token(user)
                    refresh_token = str(token)
                    access_token = str(token.access_token)
                    response = JsonResponse(
                        {
                            "message": "login success",
                            "jwt_token": {
                                "access_token": access_token,
                                "refresh_token": refresh_token,
                            },
                        },
                        status=200
                    )
                    response.set_cookie("access_token", access_token, httponly=True)
                    response.set_cookie("refresh_token", refresh_token, httponly=True)

                    return response

                return JsonResponse({'message': "비밀번호를 확인해주세요."}, status=400)

            return JsonResponse({'message': "존재하지 않는 이메일입니다."}, status=400)

        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status=400)
