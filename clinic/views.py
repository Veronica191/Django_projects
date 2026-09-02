from django.shortcuts import redirect, render
from .models import Patients, Appointments, Payments
from django.db.models import Sum
from .forms import PatientForm
from django.contrib import messages




def home(request):

    total_patients = Patients.objects.count()

    total_appointments = Appointments.objects.count()

    total_payments = Payments.objects.count()

    total_revenue = Payments.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
    }

    return render(request, 'home.html', context)


def patients(request):

    patients = Patients.objects.all()

    return render(request, 'patients.html', {
        'patients': patients
    })


def appointments(request):

    appointments = Appointments.objects.all()

    return render(request, 'appointments.html', {
        'appointments': appointments
    })


def payments(request):

    payments = Payments.objects.all()

    return render(request, 'payments.html', {
        'payments': payments
    })

def patient_form(request):

    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Patient information saved successfully.')
            return redirect('patient_form')

    else:
        form = PatientForm()

    return render(request, 'patient_form.html', {'form': form})