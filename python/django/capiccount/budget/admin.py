from django.contrib import admin

# Register your models here.

from .models import Account, Transaction, Category, Categorization

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Categorization)
admin.site.register(Transaction)
