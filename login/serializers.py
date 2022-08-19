from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=45)
    password = serializers.CharField(max_length=100)
