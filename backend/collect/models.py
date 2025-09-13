from django.db import models
from django.contrib.auth.models import User


class Collect(models.Model):
    """Модель группового сбора."""

    class Reason(models.TextChoices):
        BIRTHDAY = 'birthday', 'День рождения'
        WEDDING = 'wedding', 'Свадьба'
        MEDICAL = 'medical', 'Медицинское лечение'
        CHARITY = 'charity', 'Благотворительность'
        OTHER = 'other', 'Другое'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collects', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    reason = models.CharField(max_length=50, choices=Reason.choices, default=Reason.OTHER, verbose_name='Повод')
    description = models.TextField(blank=True, verbose_name='Описание')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Сумма сбора')
    collected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Сумма на данный момент')
    donors_count = models.PositiveIntegerField(default=0, verbose_name='Количество доноров')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Обожка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    ends_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return f"Создан сбор средств на {self.title}."
