from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patients, name='patients'),
    path('appointments/', views.appointments, name='appointments'),
    path('payments/', views.payments, name='payments'),
    path('patient-form/', views.patient_form, name='patient_form'),
]