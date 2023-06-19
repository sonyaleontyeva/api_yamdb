from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def get_confirmation_code(confirmating_user=None):
    """Генерация кода подтверждения."""

    return default_token_generator.make_token(confirmating_user)


def send_letter(email, confirmation_code):
    """Отправка письма с кодом подтверждения."""

    send_mail(
        'Письмо с кодом подтверждения',
        f'Код подтверждения - {confirmation_code}.',
        'donotreply@yamdb.ru',
        (email, ),
        fail_silently=False,
    )
