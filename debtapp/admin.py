from django.contrib import admin

from debtapp.models import Business, Customer, Debt, Payment

# Register your models here.
admin.site.register(Business)
admin.site.register(Customer)
admin.site.register(Debt)
admin.site.register(Payment)
