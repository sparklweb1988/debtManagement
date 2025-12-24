from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from debtapp.models import Business, Customer, Debt, Payment
from django.contrib.auth.models import User

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
    
    debtors = Debt.objects.all()
    total_debtors = debtors.count()
    context ={
        'total_debtors':total_debtors,
        'debtors':debtors,
        
    }
    return render(request, 'dashboard/dashboard.html',context)


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




# UPDATE pAYMENT

def update_payment(request, payment_id):
    # Get the payment object
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Get the list of customers (to populate the dropdown)
    customers = Customer.objects.all()
    
    if request.method == 'POST':
        # Get the submitted data
        customer_id = request.POST.get('customer')
        amount_paid = request.POST.get('amount_paid')
        payment_method = request.POST.get('payment_method')
        balance = request.POST.get('balance')
        status = request.POST.get('status')

        # Get the customer object from the selected ID
        customer = get_object_or_404(Customer, id=customer_id)
        
        # Update the payment object
        payment.customer = customer
        payment.amount_paid = amount_paid
        payment.payment_method = payment_method
        payment.balance = balance
        payment.status = status

        # Save the updated payment
        payment.save()
        
        # Redirect to the payment list page
        return redirect('payment_list')
    
    # If it's a GET request, render the form with the current payment data
    return render(request, 'forms/payment_update.html', {
        'payment': payment,
        'customers': customers
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
#  LOGOUT VIEW

def logout_view(request):
    logout(request)
    return redirect('home')