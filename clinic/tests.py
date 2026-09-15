from django.test import SimpleTestCase

from .forms import AppointmentForm, PaymentForm
from .models import Patients


class PatientCodeTests(SimpleTestCase):
	def test_patient_code_uses_existing_patient_id(self):
		patient = Patients(patient_insurance=100)

		self.assertEqual(patient.patient_code, 'GH100')

	def test_patient_code_is_empty_before_patient_is_saved(self):
		patient = Patients()

		self.assertEqual(patient.patient_code, '')

	def test_patient_labels_use_short_code_instead_of_uuid(self):
		patient = Patients(
			patient_insurance=100,
			first_name='Ama',
			last_name='Mensah',
			patient_uuid='12345678-1234-1234-1234-123456789012',
		)

		appointment_label = AppointmentForm.patient_label(patient)
		payment_label = PaymentForm.patient_label(patient)

		self.assertIn('GH100', appointment_label)
		self.assertIn('GH100', payment_label)
		self.assertNotIn(patient.patient_uuid, appointment_label)
		self.assertNotIn(patient.patient_uuid, payment_label)
