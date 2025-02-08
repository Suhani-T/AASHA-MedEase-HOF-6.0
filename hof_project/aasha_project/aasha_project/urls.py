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
from django.urls import path
from app1 import views

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
]



