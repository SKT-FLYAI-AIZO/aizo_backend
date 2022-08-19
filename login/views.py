import json
import bcrypt
import jwt

from account.models import Account
from aizo_backend.settings import SECRET_KEY

from django.views import View
from django.http import HttpResponse, JsonResponse

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
                    token = jwt.encode({'user': user.id}, SECRET_KEY, algorithm='HS256')

                    return JsonResponse({"token": token}, status=200)

                return JsonResponse({'message': "비밀번호를 확인해주세요."}, status=400)

            return JsonResponse({'message': "존재하지 않는 이메일입니다."}, status=400)

        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status=400)
