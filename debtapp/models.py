from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal



class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)  # Use CharField for phone numbers
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} of {self.name}"




class Customer(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)  # Use CharField for phone numbers
    address = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=GENDER)  # Adjusted max_length

    def __str__(self):
        return f"{self.name} ({self.sex})"





class Debt(models.Model):
    STATUS = (
        ('owing', 'Owing'),
        ('paid', 'Paid'),
        ('part', 'Part'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Using DecimalField for precision
    category = models.CharField(max_length=100)
    date_collected = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS, default='owing')

    def __str__(self):
        return f"{self.customer} ({self.amount})"




class Payment(models.Model):
    PAYMENT = (
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
        ('debit card', 'Debit Card'),
    )

    STATUS = (
        ('owing', 'Owing'),
        ('paid', 'Paid'),
        ('part', 'Part'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_paid = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Using DecimalField
    payment_method = models.CharField(max_length=100, choices=PAYMENT)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # DecimalField for balance
    status = models.CharField(max_length=100, choices=STATUS, default='owing')

    def __str__(self):
        return f"{self.customer} ({self.amount_paid})"




class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Income {self.amount}"


class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Expense {self.amount}"
