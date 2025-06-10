from django.contrib import admin
from .models import  ChitFund
# Register your models here.
@admin.register(ChitFund)
class ChitFundAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'total_amount', 'monthly_amount', 'duration_months', 'is_active', 'created_at')
    search_fields = ('name', 'invite_token')
    list_filter = ('is_active', 'created_at')
    filter_horizontal = ('members',)