from django.shortcuts import redirect, render
from .models import Activity, Patients, Appointments, Payments
from django.db.models import Sum
from .forms import AppointmentForm, PatientForm, PaymentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@never_cache
@login_required
def home(request):

    total_patients = Patients.objects.count()

    total_appointments = Appointments.objects.count()

    total_payments = Payments.objects.count()

    total_revenue = Payments.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    recent_activities = Activity.objects.all()[:5]

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'recent_activities': recent_activities,
    }

    return render(request, 'home.html', context)

@never_cache
@login_required
def patients(request):

    patients = Patients.objects.all()

    return render(request, 'patients.html', {
        'patients': patients
    })

@never_cache
@login_required
def appointments(request):

    appointments = Appointments.objects.all()

    return render(request, 'appointments.html', {
        'appointments': appointments
    })


@never_cache
@login_required
def appointment_form(request):

    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save()

            patient = appointment.patient_insurance

            patient_name = f'{patient.first_name} {patient.last_name}'

            doctor = appointment.doctor_name or 'the clinic team'

            Activity.objects.create(
                activity_type='appointment',
                description=(
                    f'New appointment scheduled for {patient_name} '
                    f'with {doctor}.'
                )
            )

            messages.success(
                request,
                'Appointment saved successfully.'
            )

            return redirect('home')

    else:
        form = AppointmentForm()

    return render(
        request,
        'appointment_form.html',
        {'form': form}
    )


@never_cache
@login_required
def payments(request):

    payments = Payments.objects.all()

    return render(request, 'payments.html', {
        'payments': payments
    })


@never_cache
@login_required
def patient_form(request):

    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = form.save()

            Activity.objects.create(
                activity_type='patient',
                description=(
                    f'New patient registered: '
                    f'{patient.first_name} {patient.last_name}'
                )
            )

            messages.success(
                request,
                'Patient information saved successfully.'
            )

            return redirect('patient_form')

    else:
        form = PatientForm()

    return render(
        request,
        'patient_form.html',
        {'form': form}
    )


@login_required
def payment_form(request):

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save()

            Activity.objects.create(
                activity_type='payment',
                description=f'Payment received: GH₵{payment.amount}'
            )

            messages.success(
                request,
                'Payment recorded successfully.'
            )

            return redirect('home')

    else:
        form = PaymentForm()

    return render(
        request,
        'payment_form.html',
        {'form': form}
    )


def logout_view(request):

    logout(request)

    return redirect('login')