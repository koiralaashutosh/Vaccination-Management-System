from django.contrib import admin
from .models import *
# importing all classes from models

# Register your models here.
admin.site.register(Child)
admin.site.register(Vaccination)
admin.site.register(Appointment)

