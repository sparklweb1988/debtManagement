from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from debtapp.models import Business, Customer, Debt, Expenditure, Income, Payment
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from collections import defaultdict


# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def signup_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        if password != confirm_password:
            messages.error(request, 'Password and confirm_password not match')
        
        user =User.objects.create_user(username,email,password)
        user.save()
        return redirect('signin')
    return render(request, 'accounts/signup.html')


def signin_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/signin.html')


#  LIST VIEW

def dashboard_view(request):
    # Get the current date and calculate the start of the month
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Calculate total debtors
    debtors = Debt.objects.all()
    total_debtors = debtors.count()

    # Calculate total income for the current month
    total_income = Income.objects.filter(
        user=request.user,
        date__gte=start_of_month,
        date__lte=today
    ).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    # Calculate total expenditure for the current month
    total_expenditure = Expenditure.objects.filter(
        user=request.user,
        date__gte=start_of_month,
        date__lte=today
    ).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    # Calculate profit (income - expenditure)
    profit = total_income - total_expenditure

    # Prepare context to pass to the template
    context = {
        'total_debtors': total_debtors,
        'total_income': total_income,
        'total_expenditure': total_expenditure,
        'profit': profit,
    }

    return render(request, 'dashboard/dashboard.html', context)





def bussiness_view(request):
    if request.user.is_superuser:
     
        buss = Business.objects.all().order_by('-date_created')
    else:

        buss = Business.objects.filter(owner=request.user)
    
    context = {
        'buss': buss
    }
    return render(request, 'tables/bussiness_list.html', context)



def customer_view(request):
    if request.user.is_superuser:
        cust = Customer.objects.all().order_by('-name')
        
    else:
        cust = Customer.objects.filter(user = request.user).order_by('-name')
  
        

    context = {
        'cust':cust
    }
    return render(request, 'tables/customer_list.html',context)



def debt_view(request):
    if request.user.is_superuser:
        debts = Debt.objects.all().order_by('-date_collected')
        
    else:
        debts = Debt.objects.filter(user=request.user).order_by('-date_collected')
  
        
    context = {
        'debts':debts
    }
    return render(request, 'tables/debt_list.html',context)




def payment_view(request):
    if request.user.is_superuser:
        payments = Payment.objects.all().order_by('-date_paid')
   
        
    else:
        payments = Payment.objects.filter(user=request.user).order_by('-date_paid')
    context = {
        'payments':payments
    }
    return render(request, 'tables/payment_list.html',context)


# FORM VIEW

def customer_form(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
       
        customer = Customer.objects.create(  user=request.user,name=name,email=email,phone=phone,address=address,sex=sex)
        customer.save()
        return redirect('customer_list')
    return render(request,'forms/customer_form.html')



#  DEBT
def debt_form(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    customers = Customer.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        customer_id = request.POST.get('customer')
        
        try:
            customer = Customer.objects.get(id=customer_id)
            # Create Debt instance without needing to call .save() explicitly
            Debt.objects.create(amount=amount, category=category, customer=customer,user=request.user)
            return redirect('debt_list')  # Redirect to debt list page
        except Customer.DoesNotExist:
            return render(request, 'forms/debt_form.html', {'customers': customers, 'error': 'Customer not found.'})

    return render(request, 'forms/debt_form.html', {'customers': customers})




# PAYMENT FORM
def payment_form(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    customers = Customer.objects.all()

    if request.method == 'POST':
        amount_paid = request.POST.get('amount_paid')
        payment_method = request.POST.get('payment_method')
        balance = request.POST.get('balance')
        customer_id = request.POST.get('customer')
        
       
        customer = Customer.objects.get(id=customer_id)
        payments = Payment.objects.create(amount_paid=amount_paid, payment_method=payment_method,balance=balance, customer=customer,user=request.user)
        
        
        return redirect('payment_list') 
    return render(request, 'forms/payment_form.html',{'customers':customers})



#  MARK PAID


def update_payment_status(request, id, status):
    # Ensure the status is valid
    if status not in ['paid', 'part']:
        return redirect('payment_list')  # Invalid status, just redirect

    # Get the Payment object by ID
    payment = get_object_or_404(Payment, pk=id)
    
    # Update the Payment's status
    payment.status = status
    payment.save()

    # Update the related Debt statuses to match the Payment status
    debts = Debt.objects.filter(payment=payment)
    debts.update(status=status)  # Update debt status to match payment status

    return redirect('payment_list')






#  UPDATE VIEW

def customer_update(request,id):
    customers = get_object_or_404(Customer, pk=id)
    if request.method =='POST':
        customers.name = request.POST.get('name')
        customers.email = request.POST.get('email')
        customers.phone = request.POST.get('phone')
        customers.address = request.POST.get('address')
        customers.sex = request.POST.get('sex')
       
        customers.save()
        return redirect('customer_list')
    return render(request,'forms/customer_update.html',{'customers':customers})



#  DEBTOR
def debt_update(request,id):
    debt = get_object_or_404(Debt, pk=id)
    customers = Customer.objects.all()
    
    if request.method =='POST':
        debt.amount = request.POST.get('amount')
        debt.category = request.POST.get('category')
        debt.customer_id = request.POST.get('customer')
        
        debt.save()
        return redirect('debt_list') 
    return render(request,'forms/debt_update.html',{'debt':debt,'customers':customers})




# UPDATE PAYMENT

def update_payment(request, payment_id):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    payment = get_object_or_404(Payment, id=payment_id)
    customers = Customer.objects.all()

    if request.method == 'POST':
        amount_paid = Decimal(request.POST.get('amount_paid'))
        amount_collected = Decimal(request.POST.get('balance'))  # Assuming you want to update the amount collected
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        customer_id = request.POST.get('customer')
        
        # Get the customer object based on the provided customer_id
        customer = Customer.objects.get(id=customer_id)

        # Update the payment object
        payment.amount_collected = amount_collected
        payment.amount_paid = amount_paid
        payment.payment_method = payment_method
        payment.status = status
        payment.customer = customer
        
        # Save the changes
        payment.save()

        # Redirect to payment list
        return redirect('payment_list')

    return render(request, 'forms/payment_update.html', {
        'payment': payment,
        'customers': customers
    })

#  UPDATE INCOME

def update_income(request, id):
    # Get the income object based on income_id
    income = get_object_or_404(Income, pk=id)
    
    if request.method == 'POST':
        # Get the updated amount and description from the form
        amount = Decimal(request.POST.get('amount'))
        description = request.POST.get('description')

        # Update the income fields
        income.amount = amount
        income.description = description
        
        # Save the updated income object
        income.save()
        
        # Redirect to the income list page after saving
        return redirect('income')

    # If it's a GET request, pre-populate the form with the existing data
    return render(request, 'forms/update_income.html', {
        'income': income
    })



#  UPDATE EXPENDITURE

def update_expenditure(request, id):
    # Get the expenditure object by ID
    expenditure = get_object_or_404(Expenditure, pk=id)
    
    if request.method == 'POST':
        # Get the updated amount and description from the form
        amount = Decimal(request.POST.get('amount'))
        description = request.POST.get('description')

        # Update the expenditure fields
        expenditure.amount = amount
        expenditure.description = description
        
        # Save the updated expenditure object
        expenditure.save()

        # Redirect to the expenditure list after saving
        return redirect('expenditure')

    # If it's a GET request, pre-populate the form with the current data
    return render(request, 'forms/update_expenditure.html', {
        'expenditure': expenditure
    })
    
    

#  DELETE VIEW

def customer_delete(request,id):
    customer = get_object_or_404(Customer, pk=id)
    customer.delete()
    return redirect('customer_list')


def debt_delete(request,id):
    debtors = get_object_or_404(Debt, pk=id)
    debtors.delete()
    return redirect('debt_list')

def payment_delete(request, id):
    payment = get_object_or_404(Payment, pk=id)
    payment.delete()
    return redirect('payment_list')


def delete_view(request, id):
    incomes = get_object_or_404(Income, pk=id)
    incomes.delete()
    return redirect('income')


def expenditure_delete_view(request, id):
    expense = get_object_or_404(Expenditure, pk=id)
    expense.delete()
    return redirect('expenditure')




#  INCOME


def income_view(request):
    today = timezone.now()
    month = today.month
    year = today.year

    incomes = Income.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    total_income = sum(i.amount for i in incomes)

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        Income.objects.create(
            user=request.user,
            amount=amount,
            description=description
        )
        return redirect("income")

    return render(request, "tables/income.html", {
        "incomes": incomes,
        "total_income": total_income,
    })



# EXPENDITURE

def expenditure_view(request):
    today = timezone.now()
    month = today.month
    year = today.year

    expenditures = Expenditure.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    total_expenditure = sum(e.amount for e in expenditures)

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        Expenditure.objects.create(
            user=request.user,
            amount=amount,
            description=description
        )
        return redirect("expenditure")

    return render(request, "tables/expenditure.html", {
        "expenditures": expenditures,
        "total_expenditure": total_expenditure,
    })




def logout_view(request):
    logout(request)
    return redirect('home')