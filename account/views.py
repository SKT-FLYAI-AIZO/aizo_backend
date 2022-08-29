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

    def delete(self, request):
        email = request.GET.get('email')
        if email is None:
            return JsonResponse({"message": "There is no email..."}, status=400)

        record = Account.objects.get(email=email)
        record.delete()

        return JsonResponse({"message": "Account email '{}' deleted!".format(email)}, status=200)

    def put(self, request):
        req_data = json.loads(request.body)

        email = req_data.get('email')
        if email is None:
            return JsonResponse({"message": "There is no email..."}, status=400)

        data = Account.objects.get(email=email)
        serializer = AccountSerializer(instance=data, data=req_data)
        try:
            if serializer.is_valid():
                serializer.save()

                return JsonResponse({"message": "Account email '{}' updated!".format(email)}, status=200)
        except Exception as e:
            return JsonResponse({"message": "Update failed", "message": str(e)}, status=400)
