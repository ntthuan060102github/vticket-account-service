from rest_framework import serializers
from vticket_app.enums.gender_enum import GenderEnum

class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=False)
    gender = serializers.ChoiceField(required=False, choices=list(set(GenderEnum.values)))
    birthday = serializers.DateField(required=False)
    phone_number = serializers.CharField(required=False)