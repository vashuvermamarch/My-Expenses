from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # The createsuperuser command passes is_staff=True. We pop it
        # from the extra_fields so it doesn't cause an error.
        extra_fields.pop('is_staff', None)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    # Add the new is_user field
    is_user = models.BooleanField(default=True, verbose_name='user status')

    objects = UserManager()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # All superusers are staff
        return self.is_superuser