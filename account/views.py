import json
import bcrypt

from .models import Account

from django.views import View
from django.http import JsonResponse

from .serializers import AccountSerializer


class AccountView(View):
    def post(self, request):
        try:
            serializer = AccountSerializer(data=json.loads(request.body))
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
        except Exception:
            return JsonResponse(serializer.errors, status=400)

        try:
            Account.objects.create(
                email=data['email'],
                name=data['name'],
                password=bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            ).save()

            return JsonResponse({"message": "Account Created!"}, status=201)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
