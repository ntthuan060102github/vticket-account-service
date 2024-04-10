from rest_framework import serializers

class ChangePasswordValidator(serializers.Serializer):
    old_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False)