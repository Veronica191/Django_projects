from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('patients/', views.patients, name='patients'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointment-form/', views.appointment_form, name='appointment_form'),
    path('payments/', views.payments, name='payments'),
    path('payment-form/', views.payment_form, name='payment_form'),
    path('patient-form/', views.patient_form, name='patient_form'),
] 