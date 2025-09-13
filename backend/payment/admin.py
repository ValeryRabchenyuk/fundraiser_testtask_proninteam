from django.contrib import admin


from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'collect',
        'donor',
        'amount',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = ('author__username', 'collect', 'created_at')
