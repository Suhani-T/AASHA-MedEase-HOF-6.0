from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model  
from .models import Doctor, Patient 
from django.http import JsonResponse
from django.db.models import Q

from .models import Appointment
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

CustomUser = get_user_model()


def doctor_registration(request):
    if request.method == "POST":
        # Personal Information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = f"{first_name} {last_name}"
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')

        # Professional Details
        license_number = request.POST.get('license_number')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        workplace = request.POST.get('workplace')
        address = request.POST.get('address')

        # Availability & Scheduling
        consultation_mode = request.POST.get('consultation_mode')
        available_days = request.POST.getlist('available_days')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        max_patients = request.POST.get('max_patients')

        # Document Uploads
        medical_degree = request.FILES.get('medical_degree')
        government_id = request.FILES.get('government_id')
        medical_license = request.FILES.get('medical_license')

        # Login Credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse("Passwords do not match. Please try again.")

        # Create Doctor User
        user = CustomUser.objects.create_user(
            username=username, email=email, password=password,
            
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_doctor = True 
        user.save()
        # user.save()

        # Save Doctor Information
        Doctor.objects.create(
            user=user, full_name=full_name, phone=phone, dob=dob, gender=gender,
            license_number=license_number, specialization=specialization,
            experience=experience, workplace=workplace, address=address,
            consultation_mode=consultation_mode, available_days=available_days,
            start_time=start_time, end_time=end_time, max_patients=max_patients,
            medical_degree=medical_degree, government_id=government_id, medical_license=medical_license
        )

        return redirect('login')
    return render(request, 'docsignup.html')

# Patient Registration View
def patient_registration(request):
    if request.method == "POST":
        # Personal Information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = f"{first_name} {last_name}"
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = f"{request.POST.get('address')}, {request.POST.get('city')}, {request.POST.get('state')} - {request.POST.get('pin_code')}"
        emergency_contact = request.POST.get('emergency_contact')

        # Health & Insurance Details
        blood_group = request.POST.get('blood_group')
        pre_existing_conditions = request.POST.get('pre_existing_conditions')
        current_medications = request.POST.get('current_medications')
        allergies = request.POST.get('allergies')
        preferred_doctor = request.POST.get('preferred_doctor')
        insurance_provider = request.POST.get('insurance_provider')
        policy_number = request.POST.get('policy_number')
        coverage_type = request.POST.get('coverage_type')

        # Login Credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse("Passwords do not match. Please try again.")

        if CustomUser.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose another.")

        
        profile_picture = request.FILES.get('profile_picture')

        short_bio = request.POST.get('short_bio', '')  
        languages_spoken = request.POST.get('languages_spoken', '')

        
        consultation_mode = request.POST.get('preferred_consultation_mode')
        
        user = CustomUser.objects.create_user(
            username=username, email=email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_patient = True 
        user.save()

       
        Patient.objects.create(
            user=user, full_name=full_name, phone=phone, dob=dob, gender=gender,
            address=address, emergency_contact=emergency_contact,
            blood_group=blood_group, pre_existing_conditions=pre_existing_conditions,
            current_medications=current_medications, allergies=allergies,
            preferred_doctor=preferred_doctor, insurance_provider=insurance_provider,
            policy_number=policy_number, coverage_type=coverage_type,
            profile_picture=request.FILES.get('profile_picture'),
            bio=request.POST.get('short_bio'), languages_spoken=request.POST.get('languages_spoken'),
            consultation_mode=request.POST.get('preferred_consultation_mode')
        )
        return redirect('login')
    return render(request, 'patsignup.html')

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request, username=username, password=password)

        if user and user.is_authenticated:
            if role == 'doctor' and user.is_doctor:
                if Doctor.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('homepage2doc')
                messages.error(request, 'Doctor profile not found.')
            elif role == 'patient' and user.is_patient:
                if Patient.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('homepage2pat')
                messages.error(request, 'Patient profile not found.')
            else:
                messages.error(request, 'Invalid role selected.')
        else:
            messages.error(request, 'Invalid username or password.')
        return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')


def doctor_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    doctor = Doctor.objects.filter(user=request.user).first()
    if doctor:
        return render(request, 'doctor_profile.html', {'doctor': doctor})
    messages.error(request, 'Doctor profile not found.')
    return redirect('login')

def patient_profile(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    
    patient = Patient.objects.filter(id=pk).first()
    if patient:
        return render(request, 'patient_profile.html', {'patient': patient})
    
    messages.error(request, 'Patient profile not found.')
    return redirect('login')

def patient_profile_actual(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient_profile.html', {'patient': patient})


def doctor_profile_actual(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor_profile.html', {'doctor': doctor})




def patient_dashboard(request):
    return render(request, 'pat_dashboard.html')

def homepage(request):
    return render(request, 'homepage1.html')

def signupask(request):
    return render(request, 'signupask.html')

@login_required(login_url='login')
def homepage2doc(request):
    return render(request, 'homepage2doc.html')

@login_required(login_url='login')
def homepage2pat(request):
    return render(request, 'homepage2pat.html')


def search_doctors(request):
    query = request.GET.get("q", "").strip()
    
    if query:
        doctors = Doctor.objects.filter(
            Q(full_name__icontains=query) | Q(specialization__icontains=query)
        )[:5]  

       
        
        
        results = [
            {
                "id": doctor.id,
                "full_name": doctor.full_name,
                "specialization": doctor.specialization,
                "workplace": doctor.workplace
            }
            for doctor in doctors
        ]
    else:
        results = []

    return JsonResponse({"results": results})


def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_profile.html', {'doctor': doctor})


@login_required
def doctor_dashboard(request):

    doctor = get_object_or_404(Doctor, user=request.user)
    today = timezone.now().date()

    
    todays_appointments = (
        Appointment.objects.filter(doctor=doctor, date=today)
        .order_by("time")
        .select_related("patient")
    )

   
    upcoming_appointments = (
        Appointment.objects.filter(doctor=doctor, date__gt=today)
        .order_by("date")
        .select_related("patient")
    )

    return render(
        request,
        "doc_dashboard.html",
        {
            "doctor": doctor,
            "todays_appointments": todays_appointments,
            "upcoming_appointments": upcoming_appointments,
        },
    )

@login_required
def book_appointment(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        doctor = None

       
        appointment_date = request.POST.get("date")
        if appointment_date < str(timezone.now().date()): 
            messages.error(request, "Cannot book an appointment for a past date.")
            return redirect(request.META.get('HTTP_REFERER', 'pat_dashboard'))

        
        try:
            doctor = Doctor.objects.get(full_name__iexact=doctor_name)  
        except Doctor.DoesNotExist:
            doctor = Doctor.objects.create(full_name=doctor_name)  

       
        appointment = Appointment.objects.create(
            patient=request.user.patient_profile,
            doctor=doctor,
            reason=request.POST.get("reason"),
            date=appointment_date,
            mode=request.POST.get("mode")
        )


        return redirect(request.META.get('HTTP_REFERER', 'pat_dashboard'))

    return redirect("pat_dashboard")

@login_required
def patient_dashboard(request):
    """Fetch the current appointment and upcoming appointments for the logged-in patient."""
    patient = request.user.patient_profile  
    today = timezone.now().date()

    
    current_appointment = Appointment.objects.filter(
        patient=patient,
        date=today,
        is_completed=False
    ).order_by('id').first()  

    
    queue_position = None
    if current_appointment:
        

        queue_position = Appointment.objects.filter(
            doctor=current_appointment.doctor,
            date=today,
            
            id__lt=current_appointment.id  
        ).count()

    
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        is_completed=False,
        date__gt=today
    ).order_by('date', 'id')  

    return render(request, 'pat_dashboard.html', {
        'current_appointment': current_appointment,
        'upcoming_appointments': upcoming_appointments,
        'queue_position': queue_position 
    })


@csrf_protect
@require_POST
@login_required
def mark_appointment_completed(request, appointment_id):
    
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.doctor.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    appointment.is_completed = data.get('is_completed', False)
    appointment.save()

    return JsonResponse({'success': True, 'completed': appointment.is_completed})