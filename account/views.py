import json
import bcrypt

from .models import Account

from django.views import View
from django.http import HttpResponse, JsonResponse


class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EXISTS_EMAIL"}, status=400)

            Account.objects.create(
                email=data['email'],
                name=data['name'],
                password=bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            ).save()

            return HttpResponse({"message : Account Created!"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status=400)
