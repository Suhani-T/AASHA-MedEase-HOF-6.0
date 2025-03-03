"""
URL configuration for aasha_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app1 import views

from app1.views import search_doctors
from app1.views import doctor_profile
from app1.views import logout_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.homepage, name='homepage'),
    

    path('signupask/', views.signupask, name='signupask'),

    path('doctor/register/', views.doctor_registration, name='doctor_registration'),
    
    
    path('patient/register/', views.patient_registration, name='patient_registration'),
    
    
    path('login/', views.login_view, name='login'),
    
    
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    
    
    path('patient/profile/', views.patient_profile, name='patient_profile'),

    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    path('homepage2doc/', views.homepage2doc, name='homepage2doc'),
    path('homepage2pat/', views.homepage2pat, name='homepage2pat'),

    path("search_doctors/", search_doctors, name="search_doctors"),

    path('doctor/<int:doctor_id>/', doctor_profile, name='doctor_profile'),
    path('patient/patient_dashboard/<int:doctor_id>/', views.patient_dashboard, name='patient_dashboard'),

    path('logout/', logout_view, name='logout'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),

    path('patient/<int:pk>/', views.patient_profile, name='patient_profile'),
    path('mark_appointment_completed/<int:appointment_id>/', views.mark_appointment_completed, name='mark_appointment_completed'),

    
    path('patient/profile/<int:pk>/', views.patient_profile_actual, name='patient_profile_actual'),
    path('doctor/profile/<int:pk>/', views.doctor_profile_actual, name='doctor_profile_actual'),

    path('mark_appointment_completed/<int:appointment_id>/', views.mark_appointment_completed, name='mark_appointment_completed'),

    path("chatbot/", views.chatbot_api, name="chatbot_api"),

    path('diseases/', views.diseases_view, name='diseases'),
    path('about-us/', views.about_us, name='about_us'),
    path('faqs/', views.faqs, name='faqs'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



