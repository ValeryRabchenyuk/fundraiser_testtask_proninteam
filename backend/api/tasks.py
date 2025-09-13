from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from collect.models import Collect
from payment.models import Payment
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_collect_created_email(collect_id):
    """Отправка email о создании сбора."""
    try:
        collect = Collect.objects.select_related('author').get(id=collect_id)
        subject = f"Сбор '{collect.title}' успешно создан!"
        message = (
            f"Здравствуйте, вы запустили сбор {collect.title}.\n"
            f"Запланированная сумма: {collect.target_amount}\n"
            f"Дата окончания: {collect.ends_at}\n\n"
            f"Спасибо, что используете наш сервис!"
        )
        recipient = collect.author.email
        if recipient and recipient.strip():
            send_mail(subject, message, 'no-reply@fundraiser.com', [recipient], fail_silently=False)
    except Collect.DoesNotExist:
        logger.error(f"Ошибка при отправке письма автору сбора {collect_id}.")


@shared_task
def send_payment_notification(payment_id):
    """Отправка email о платеже."""
    try:
        payment = Payment.objects.select_related('donor', 'collect').get(id=payment_id)
        subject = f"Вы поддержали сбор: {payment.collect.title}"
        message = (
            f"Здравствуйте, вы отправили {payment.amount}₽ "
            f"на сбор '{payment.collect.title}'.\n"
            f"Дата: {payment.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Спасибо за поддержку!"
        )
        recipient = payment.donor.email
        if recipient and recipient.strip():
            send_mail(subject, message, 'no-reply@fundraiser.com', [recipient], fail_silently=False)
    except Payment.DoesNotExist:
        logger.error(f"Ошибка при отправке письма донеру платежа {payment_id}.")
