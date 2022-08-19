import json
import bcrypt
import jwt

from account.models import Account
from aizo_backend.settings import SECRET_KEY

from django.views import View
from django.http import HttpResponse, JsonResponse


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email=data["email"]).exists():
                user = Account.objects.get(email=data["email"])

                if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                    token = jwt.encode({'user': user.id}, SECRET_KEY, algorithm='HS256')

                    return JsonResponse({"token": token}, status=200)

                return HttpResponse(status=401)

            return HttpResponse(status=400)

        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status=400)
