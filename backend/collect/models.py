from django.db import models
from django.contrib.auth.models import User


class Collect(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('medical', 'Медицинское лечение'),
        ('charity', 'Благотворительность'),
        ('other', 'Другое'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collects')
    title = models.CharField(max_length=200)
    reason = models.CharField(max_length=50, choices=OCCASION_CHOICES)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # null = infinite
    collected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    donors_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_unlimited(self):
        return self.target_amount is None

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    