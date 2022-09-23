from rest_framework import serializers

class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500)


