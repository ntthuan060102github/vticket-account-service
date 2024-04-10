from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from vticket_app.enums.role_enum import RoleEnum
from vticket_app.enums.gender_enum import GenderEnum
from vticket_app.enums.account_status_enum import AccountStatusEnum

from django.contrib.auth.base_user import BaseUserManager

class User(AbstractBaseUser):
    class Meta:
        db_table = "user"
        app_label = "vticket_app"
        
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    gender = models.SmallIntegerField(choices=GenderEnum.choices, default=GenderEnum.PRIVATE)
    birthday = models.DateField(null=True)
    avatar_url = models.CharField(max_length=1500, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=50, choices=AccountStatusEnum.choices, null=False)
    role = models.CharField(max_length=20, choices=RoleEnum.choices, null=False, default=RoleEnum.CUSTOMER)

    USERNAME_FIELD = "email"

    objects = BaseUserManager()