from rest_framework import serializers

from account.models import Account, Alarm


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'name',
            'email',
            'password'
        )


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = (
            'content',
            'is_read'
        )