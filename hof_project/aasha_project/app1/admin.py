from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Patient,Appointment

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)

class CustomUserAdmin(UserAdmin):  
    list_display = ('username', 'email', 'is_doctor', 'is_patient', 'is_active', 'is_staff')  
    list_filter = ('is_doctor', 'is_patient', 'is_active')    
    search_fields = ('username', 'email')  

admin.site.register(CustomUser, CustomUserAdmin) 

