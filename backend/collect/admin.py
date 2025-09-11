from django.contrib import admin


from .models import Collect

@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'title',
        'reason',
        'target_amount',
        'collected_amount',
        'donors_count',
        'created_at',
        'ends_at'
    )
    list_filter = ('author', 'reason', 'created_at', 'ends_at')
    search_fields = ('author__username', 'title', 'created_at')
    list_editable = ('title', 'reason', 'target_amount', 'ends_at')
