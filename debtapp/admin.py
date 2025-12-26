from django.contrib import admin

from debtapp.models import Business, Customer, Debt, Expenditure, Income, Payment

# Register your models here.
admin.site.register(Business)
admin.site.register(Customer)
admin.site.register(Debt)
admin.site.register(Payment)
admin.site.register(Income)
admin.site.register(Expenditure)
