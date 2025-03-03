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

import os
import joblib 
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'wait_time_model.joblib')
ENCODER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'spec_encoder.joblib')

waiting_time_model = joblib.load(MODEL_PATH)
spec_encoder = joblib.load(ENCODER_PATH)

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
        profile_picture=request.FILES.get('profile_picture')

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
            medical_degree=medical_degree, government_id=government_id, medical_license=medical_license,
            profile_picture=profile_picture
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
        city=request.POST.get('city')
        state=request.POST.get('state')
        pin_code=request.POST.get('pin_code')
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
        profile_picture=request.FILES.get('profile_picture')

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
            city=city,state=state,pin_code=pin_code,
            address=address, emergency_contact=emergency_contact,
            blood_group=blood_group, pre_existing_conditions=pre_existing_conditions,
            current_medications=current_medications, allergies=allergies,
            preferred_doctor=preferred_doctor, insurance_provider=insurance_provider,
            policy_number=policy_number, coverage_type=coverage_type,
            profile_picture=profile_picture,
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


def patient_profile_actual(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient_profile.html', {'patient': patient})

def doctor_profile_actual(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor_profile.html', {'doctor': doctor})



@login_required
def patient_dashboard(request):
    """Fetch the current appointment, upcoming appointments, and predicted waiting time for the logged-in patient."""
    patient = request.user.patient_profile  # Get the logged-in patient
    today = timezone.now().date()

    # Define specializations and their average checkup times
    specialisations = {
        "ENT": 15, "Optical": 10,
        "Cardiology": 25, "Orthopedics": 30, 
        "Pediatrics": 20, "Neurology": 35,
        "Dermatology": 15, "Gastroenterology": 25,
        "Oncology": 40, "Psychiatry": 45,
        "Gynecology": 20, "Dentistry": 15,
        "Urology": 30, "Endocrinology": 25,
        "Ophthalmology": 10, "Rheumatology": 30,
        "Pulmonology": 20, "Nephrology": 30,
        "Hematology": 35, "Infectious Disease": 25,
        "Plastic Surgery": 60, "Anesthesiology": 20,
        "Emergency Medicine": 10, "Pathology": 15, 
        "Radiology": 20, "Palliative Care": 30
    }

    # Get the current appointment for today (if any)
    current_appointment = Appointment.objects.filter(
        patient=patient,
        date=today,
        is_completed=False
    ).order_by('id').first()

    # Get upcoming appointments (appointments scheduled after today)
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        date__gt=today,
    ).order_by('date', 'id')

    # Initialize values
    queue_position = None
    predicted_time = None

    if current_appointment:
        # Count the number of patients ahead in the queue
        queue_position = Appointment.objects.filter(
            doctor=current_appointment.doctor,
            date=today,
            id__lt=current_appointment.id,
            is_completed=False
        ).order_by('id').count()

        if queue_position == 0:
            predicted_time = "It's your turn!"
        elif current_appointment.doctor:
            specialization = current_appointment.doctor.specialization

            try:
                specialization_encoded = spec_encoder.transform([specialization])[0]

                # Ensure specialization exists in the dictionary before accessing
                if specialization in specialisations:
                    avg_time_per_checkup = specialisations[specialization]
                    features = [[specialization_encoded, queue_position, avg_time_per_checkup]]

                    # Predict waiting time with all features
                    predicted_time = round(waiting_time_model.predict(features)[0])

                else:
                    print(f"Warning: Specialization '{specialization}' not found in dictionary.")

            except Exception as e:
                print(f"Error in specialization encoding or prediction: {e}")

    return render(request, 'pat_dashboard.html', {
        'current_appointment': current_appointment,
        'upcoming_appointments': upcoming_appointments,
        'queue_position': queue_position,
        'predicted_time': predicted_time
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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import get_chatbot_response  # Import chatbot function

@csrf_exempt  # Disable CSRF for simplicity (use authentication in production)
def chatbot_api(request):
    if request.method == "GET":
        query = request.GET.get("query", "")
        if not query:
            return JsonResponse({"error": "No query provided"}, status=400)
        
        response = get_chatbot_response(query)
        return JsonResponse({"response": response})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def diseases_view(request):
    letter = request.GET.get('letter', '')  # Get 'letter' from URL
    return render(request, 'disease.html', {'letter': letter})

def about_us(request):
    return render(request, 'About us.html')  # Renders 'about_us.html'

def faqs(request):
    return render(request, 'faq\'s.html')