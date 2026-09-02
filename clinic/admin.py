from django.contrib import admin
from .models import Patients, Appointments, Payments


@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):
    list_display = (
        'patient_insurance',
        'first_name',
        'last_name',
        'gender',
        'phone',
        'registration_date'
    )


@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = (
        'appointment_id',
        'patient_insurance',
        'appointment_date',
        'appointment_time',
        'doctor_name',
        'status'
    )


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id',
        'patient_insurance',
        'appointment',
        'amount',
        'payment_date',
        'payment_method',
        'payment_status'
    )