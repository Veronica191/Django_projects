from django.db import models


class Patients(models.Model):
    patient_insurance = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    registration_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'patients'


class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient_insurance = models.ForeignKey(
        Patients,
        models.DO_NOTHING,
        db_column='patient_insurance'
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField(blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'appointments'


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    patient_insurance = models.ForeignKey(
        Patients,
        models.DO_NOTHING,
        db_column='patient_insurance'
    )
    appointment = models.ForeignKey(
        Appointments,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'payments'
