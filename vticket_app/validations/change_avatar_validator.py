from rest_framework import serializers

class ChangeAvatarValidator(serializers.Serializer):
    image = serializers.ImageField()