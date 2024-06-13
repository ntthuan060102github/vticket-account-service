from rest_framework import serializers

class GetUsersValidation(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())