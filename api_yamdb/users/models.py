from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, blank=False,
                                validators=(RegexValidator(r'^[\w.@+-]+\z',),))
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

    # confirmation_code = models.IntegerField(blank=True, default=0)

    # user_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:settings.USERNAME_LENGTH]

    def is_moderator(self):
        return self.role == 'moderator'

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'
