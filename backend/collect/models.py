from django.db import models
from django.contrib.auth.models import User

from fundraiser.constants import (
    TITLE_MAX_LENGTH,
    REASON_MAX_LENGTH,
    MAX_AMOUNT_NUMBER,
    DEFAULT_NUMBER,
    DECIMAL_NUMBER
)


class Collect(models.Model):
    """Модель группового сбора."""

    class Reason(models.TextChoices):
        BIRTHDAY = 'birthday', 'День рождения'
        WEDDING = 'wedding', 'Свадьба'
        MEDICAL = 'medical', 'Медицинское лечение'
        CHARITY = 'charity', 'Благотворительность'
        OTHER = 'other', 'Другое'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collects', verbose_name='Автор')
    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Название')
    reason = models.CharField(max_length=REASON_MAX_LENGTH, choices=Reason.choices, default=Reason.OTHER, verbose_name='Повод')
    description = models.TextField(blank=True, verbose_name='Описание')
    target_amount = models.DecimalField(max_digits=MAX_AMOUNT_NUMBER, decimal_places=DECIMAL_NUMBER, null=True, blank=True, verbose_name='Сумма сбора')
    collected_amount = models.DecimalField(max_digits=MAX_AMOUNT_NUMBER, decimal_places=DECIMAL_NUMBER, default=DEFAULT_NUMBER, verbose_name='Сумма на данный момент')
    donors_count = models.PositiveIntegerField(default=DEFAULT_NUMBER, verbose_name='Количество доноров')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Обожка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    ends_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return f"Создан сбор средств на {self.title}."
