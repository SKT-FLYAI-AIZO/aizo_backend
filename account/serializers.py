from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'name',
            'email',
            'password'
        )
