import json
import bcrypt

from .models import Account, Alarm

from django.core import serializers
from django.views import View
from django.http import JsonResponse

from .serializers import AccountSerializer, AlarmSerializer


class AccountView(View):
    def get(self, request):
        email = request.GET.get('email')
        if email is None:
            return JsonResponse({"message": "There is no email..."}, status=400)

        record = Account.objects.get(email=email)
        name = record.name

        return JsonResponse({"message": "Get name success!", "name": name}, status=200)

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

        name = req_data.get('name')
        password = req_data.get('password')

        if name is None and password is None:
            return JsonResponse({"message": "There is no name and password..."}, status=400)

        query = Account.objects.filter(email=email)

        if name is None:
            name = query.get().name

        if password is None:
            password = query.get().password

        password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")

        update_data = {"email": email, "name": name, "password": password}

        data = Account.objects.get(email=email)
        serializer = AccountSerializer(instance=data, data=update_data)
        try:
            if serializer.is_valid():
                serializer.save()

                return JsonResponse({"message": "Account email '{}' updated!".format(email)}, status=200)
        except Exception as e:
            return JsonResponse({"message": "Update failed", "message": str(e)}, status=400)


class AlarmView(View):
    def get(self, request):
        email = request.GET.get('email')
        if email is None:
            return JsonResponse({"message": "Fill the email."}, status=400)
        is_read = request.GET.get('is_read', False)

        query = Account.objects.filter(email=email).only("id")
        if query.__len__() == 0:
            return JsonResponse({"message": "There is no such email."}, status=204)
        account_id = int(query.get().id)

        data = Alarm.objects.filter(account_id_id=account_id, is_read=is_read)
        data = serializers.serialize("json", data, fields=('account_id', 'content', 'is_read'))

        return JsonResponse({"message": "Success!", "data": data}, status=200)


    def post(self, request):
        data = json.loads(request.body)

        email = data.get("email")
        if email is None:
            return JsonResponse({"message": "Fill the email."}, status=400)

        query = Account.objects.filter(email=data.get("email")).only("id")
        if query.__len__() == 0:
            return JsonResponse({"message": "There is no such email."}, status=204)
        account_id = int(query.get().id)

        Alarm.objects.create(
            content=data.get("content"),
            account_id_id=account_id,
        ).save()

        return JsonResponse({"message": "Success!"}, status=201)

    def delete(self, request):
        alarm_id = request.GET.get('alarm_id')
        if alarm_id is None:
            return JsonResponse({"message": "There is no id..."}, status=400)

        record = Alarm.objects.get(id=alarm_id)
        record.delete()

        return JsonResponse({"message": "Alarm id '{}' deleted!".format(alarm_id)}, status=200)

    def put(self, request):
        req_data = json.loads(request.body)

        alarm_id = req_data.get('alarm_id')
        content = req_data.get('content')
        is_read = req_data.get('is_read')

        if content is None and is_read is None:
            return JsonResponse({"message": "There is no content and is_read..."}, status=400)

        query = Alarm.objects.filter(id=alarm_id)

        if content is None:
            content = query.get().content

        if is_read is None:
            is_read = query.get().is_read

        update_data = {"content": content, "is_read": is_read}

        data = Alarm.objects.get(id=alarm_id)
        serializer = AlarmSerializer(instance=data, data=update_data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Alarm id '{}' updated!".format(alarm_id)}, status=200)
        except Exception as e:
            return JsonResponse({"message": "Update failed", "message": str(e)}, status=400)
