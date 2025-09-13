from django.db import models, transaction
from django.db.models import F

from collect.models import Collect
from django.contrib.auth.models import User

from collect.constants import MAX_AMOUNT_NUMBER, DECIMAL_NUMBER


class Payment(models.Model):
    """Платёж для сбора."""
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Сбор'
    )
    donor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Донор'
    )
    amount = models.DecimalField(
        max_digits=MAX_AMOUNT_NUMBER,
        decimal_places=DECIMAL_NUMBER,
        verbose_name='Сумма пожертвования'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время пожертвования'
    )

    def __str__(self):
        return f'{self.amount} -> {self.collect.title}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            with transaction.atomic():
                collect = Collect.objects.select_for_update().\
                    get(id=self.collect.id)

                is_first_payment = not Payment.objects.\
                    filter(collect=collect, donor=self.donor).exists()

                update_data = {
                    'collected_amount': F('collected_amount') + self.amount
                }

                if is_first_payment:
                    update_data['donors_count'] = F('donors_count') + 1

                Collect.objects.filter(id=collect.id).update(**update_data)

        super().save(*args, **kwargs)
