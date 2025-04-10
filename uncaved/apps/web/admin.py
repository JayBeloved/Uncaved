# Register the beta model in models.py with the Django admin site.
from django.contrib import admin
from .models import BetaTester        


@admin.register(BetaTester)
class BetaTesterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

