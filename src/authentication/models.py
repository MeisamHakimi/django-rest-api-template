import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

import logging

logger = logging.getLogger("django")


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        phone,
        password=None,
        is_blocked=False,
        is_staff=False,
        is_superuser=False,
        is_active=True,
        **kwargs,
    ):
        if username is None:
            raise TypeError("username is required!")

        if email is None:
            raise TypeError("email is required!")

        user = self.model(username=username, email=self.normalize_email(email))
        user.phone = phone
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.is_blocked = is_blocked
        user.save(using=self._db)

        return user

    def create_staffuser(self, username, email, phone, password=None, **kwargs):
        user = self.create_user(
            username=username, email=email, phone=phone, password=password, is_staff=True
        )
        return user

    def create_superuser(self, username, email, phone, password=None):
        if password is None:
            raise TypeError("password is required!")

        user = self.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255, default="")
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self) -> str:
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
