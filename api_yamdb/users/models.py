from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.TextField('Роль', blank=False, default='user')

    USERNAME_FIELD = 'username'

    def is_moderator(self):
        return self.role == 'moderator'

    def is_admin(self):
        return self.role == 'admin'
