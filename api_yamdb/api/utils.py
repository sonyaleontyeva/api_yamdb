from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from users.models import User


def get_confirmation_code(confirmating_user=None):
    """Генерация кода подтверждения."""

    return default_token_generator.make_token(confirmating_user)


def check_confirmation_code(username=None, confirmation_code=None):
    """Проверка кода подтверждения."""
    found_user = get_object_or_404(User, username=username,
                                   token=confirmation_code)
    return default_token_generator.check_token(found_user, confirmation_code)


def send_letter(email, confirmation_code):
    """Отправка письма с кодом подтверждения."""

    send_mail(
        'Письмо с кодом подтверждения',
        f'Код подтверждения - {confirmation_code}.',
        'donotreply@yamdb.ru',
        (email, ),
        fail_silently=False,
    )
