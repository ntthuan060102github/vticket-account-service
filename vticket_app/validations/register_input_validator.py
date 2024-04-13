from rest_framework import serializers

from vticket_app.enums.role_enum import RoleEnum
from vticket_app.models.user import User

class RegisterInputValidator(serializers.ModelSerializer):
    except_roles = [RoleEnum.ADMIN]

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "gender", "birthday", "password", "role")

    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=list(set(RoleEnum.values) - set(except_roles)))