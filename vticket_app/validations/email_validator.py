from rest_framework import serializers
class EmailValidation(serializers.Serializer):
    email = serializers.EmailField(required=True)