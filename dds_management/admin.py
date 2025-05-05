from django.contrib import admin
from .models import Status, TransactionType, Category, SubCategory, Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'amount')

admin.site.register([Status, TransactionType, Category, SubCategory])