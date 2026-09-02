from django import forms
from django.core.validators import RegexValidator
from datetime import date
from .models import Patients


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