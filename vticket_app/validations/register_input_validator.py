from rest_framework import serializers

from vticket_app.models.user import User

class RegisterInputValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "gender", "birthday", "password")