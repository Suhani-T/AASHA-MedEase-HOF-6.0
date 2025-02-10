

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

CONSULTATION_MODE_CHOICES = [
    ('in_person', 'In-Person'),
    ('video_call', 'Video Call'),
    ('phone_call', 'Phone Call'),
]
   
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    full_name = models.CharField(max_length=100)
   
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    license_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    workplace = models.CharField(max_length=200)
    address = models.TextField()
    consultation_mode = models.CharField(max_length=50)
    available_days = models.JSONField(default=list) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.IntegerField()
    medical_degree = models.FileField(upload_to='doctor_documents/')
    government_id = models.FileField(upload_to='doctor_documents/')
    medical_license = models.FileField(upload_to='doctor_documents/')

    def __str__(self):
        return self.full_name

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    full_name = models.CharField(max_length=100)
    
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    pre_existing_conditions = models.TextField()
    current_medications = models.TextField()
    allergies = models.TextField()
    preferred_doctor = models.CharField(max_length=100)
    insurance_provider = models.CharField(max_length=100, blank=True)
    policy_number = models.CharField(max_length=50, blank=True)
    coverage_type = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='patient_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    languages_spoken = models.CharField(max_length=100)
    consultation_mode = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    reason = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    mode = models.CharField(max_length=10, choices=CONSULTATION_MODE_CHOICES)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.full_name} on {self.date} at {self.time}"