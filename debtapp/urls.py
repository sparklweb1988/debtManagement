from django.urls import path
from . import views

urlpatterns = [
   
   #  HOME AND ACCOUTS URLS
   
   
   path('', views.home, name='home'),
   path('signup/', views.signup_view, name='signup'),
   path('signin/', views.signin_view, name='signin'),
   
   #  LOGOUT URLS
   
   path('logout/', views.logout_view, name='logout'),
   
   
   #  LIST URLS
   path('dashboard/', views.dashboard_view, name='dashboard'),
   path('bussiness/list/', views.bussiness_view, name='bussiness_list'),
   path('customer/list/', views.customer_view, name='customer_list'),
   path('debt/list/', views.debt_view, name='debt_list'),
   path('payment/list/', views.payment_view, name='payment_list'),
   
   # FORMS
   path('customer/form/', views.customer_form, name='customer_form'),
   path('debt/form/', views.debt_form, name='debt_form'),
   path('payment/form/', views.payment_form, name='payment_form'),
   
   
   # UPDATE URLS 
   
   path('customer/update/<int:id>/', views.customer_update, name='customer_update'),
   path('debt/update/<int:id>/', views.debt_update, name='debt_update'),
   path('payment/update/<int:payment_id>/', views.update_payment, name='update_payment'),
   path('income/update/<int:id>/', views.update_income, name='update_income'),
   path('expenditure/update/<int:id>/', views.update_expenditure, name='update_expenditure'),
   


   
   # TRANSACTIONS
   
   path("income/", views.income_view, name="income"),
   path("expenditure/", views.expenditure_view, name="expenditure"),

#  MARK AS PAID AND PART

   path('update_payment_status/<int:id>/<str:status>/', views.update_payment_status, name='update_payment_status'),
   
   #  DELETE URLS
   path('customer/delete/<int:id>/', views.customer_delete, name='customer_delete'),
   path('debt/delete/<int:id>/', views.debt_delete, name='debt_delete'),
   path('payment/delete/<int:id>/', views.payment_delete, name='payment_delete'),
   path('income/delete/<int:id>/', views.delete_view, name='delete'),
   path('expenditure/delete/<int:id>/', views.expenditure_delete_view, name='delete_expenditure'),
]
