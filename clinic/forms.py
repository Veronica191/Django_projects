from django import forms
from django.core.validators import RegexValidator
from datetime import date
from .models import Appointments, Patients, Payments


class PatientForm(forms.ModelForm):

    phone = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message='Enter a valid phone number.'
            )
        ]
    )

    gender = forms.ChoiceField(
        choices=[
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
    )

    class Meta:
        model = Patients
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'phone',
            'registration_date',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'registration_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not first_name.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'First name should contain letters only.'
            )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not last_name.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'Last name should contain letters only.'
            )

        return last_name

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']

        if dob > date.today():
            raise forms.ValidationError(
                'Date of birth cannot be in the future.'
            )

        return dob

    def clean_registration_date(self):
        registration_date = self.cleaned_data['registration_date']

        if registration_date > date.today():
            raise forms.ValidationError(
                'Registration date cannot be in the future.'
            )

        return registration_date


class AppointmentForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Appointments
        fields = [
            'patient_insurance',
            'appointment_date',
            'appointment_time',
            'doctor_name',
            'reason',
            'status',
        ]
        labels = {
            'patient_insurance': 'Patient',
            'appointment_date': 'Appointment date',
            'appointment_time': 'Appointment time',
            'doctor_name': 'Doctor',
            'reason': 'Reason for visit',
            'status': 'Status',
        }
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'doctor_name': forms.TextInput(attrs={'placeholder': 'e.g. Dr. Mensah'}),
            'reason': forms.TextInput(attrs={'placeholder': 'e.g. General consultation'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient_insurance'].queryset = Patients.objects.all().order_by(
            'first_name', 'last_name'
        )
        self.fields['patient_insurance'].empty_label = 'Select a patient'
        self.fields['patient_insurance'].label_from_instance = self.patient_label

    @staticmethod
    def patient_label(patient):
        return f'{patient.first_name} {patient.last_name} — ID {patient.patient_insurance}'

class PaymentForm(forms.ModelForm):

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Card', 'Card'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_status = forms.ChoiceField(
        choices=PAYMENT_STATUS_CHOICES
    )

    class Meta:
        model = Payments
        fields = [
            'patient_insurance',
            'appointment',
            'amount',
            'payment_date',
            'payment_method',
            'payment_status',
        ]

        labels = {
            'patient_insurance': 'Patient',
            'appointment': 'Appointment',
            'amount': 'Amount',
            'payment_date': 'Payment date',
            'payment_method': 'Payment method',
            'payment_status': 'Payment status',
        }

        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 150.00',
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'payment_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['patient_insurance'].queryset = Patients.objects.all().order_by(
            'first_name', 'last_name'
        )

        self.fields['patient_insurance'].empty_label = 'Select a patient'

        self.fields['patient_insurance'].label_from_instance = self.patient_label

        self.fields['appointment'].queryset = Appointments.objects.all().order_by(
            '-appointment_date'
        )

        self.fields['appointment'].empty_label = 'Select an appointment (optional)'
        self.fields['appointment'].label_from_instance = self.appointment_label

    @staticmethod
    def patient_label(patient):
        return f'{patient.first_name} {patient.last_name} — ID {patient.patient_insurance}'

    @staticmethod
    def appointment_label(appointment):
        patient = appointment.patient_insurance
        patient_name = f'{patient.first_name} {patient.last_name}'
        doctor = appointment.doctor_name or 'Clinic team'
        return f'{appointment.appointment_date} — {patient_name} with {doctor}'

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError('Amount cannot be negative.')
        return amount