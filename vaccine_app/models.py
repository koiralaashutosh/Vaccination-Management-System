from django.db import models
from datetime import time

class Child(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    parent_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200)
    medical_notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.full_name


class Vaccination(models.Model):
    vaccination_name = models.CharField(max_length=100)
    recommended_time = models.IntegerField()  # in months
    dose_number = models.IntegerField()
    vaccination_notes = models.CharField(max_length=100)

    def __str__(self):
        return self.vaccination_name


class Appointment(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField(default=time(9, 0))  # 9:00 AM default
    status = models.CharField(max_length=20, default='Scheduled')
    reminder_sent = models.BooleanField(default=False)
    reminder_datetime = models.DateTimeField(blank=True, null=True)  # New: datetime for SMS
    appointment_notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.child.full_name} - {self.vaccination.vaccination_name} at {self.scheduled_time}"
