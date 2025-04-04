from django.contrib import admin
from .models import *

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Transaction model.
    """
    list_display = ('date', 'description', 'amount', 'category', 'source')
    search_fields = ('description', 'category')
    list_filter = ('date', 'category')

# Register the Transaction model with the admin site
admin.site.register(Transaction, TransactionAdmin)

# Register the Category model with the admin site
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.
    """
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)