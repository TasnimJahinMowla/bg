from django.db import IntegrityError   # Add this import for IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from django import forms

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password != confirmpassword:
            return JsonResponse({'message': 'Passwords do not match', 'alert_type': 'danger'})

        try:
            if User.objects.get(username=username):
                return JsonResponse({'message': 'Username is taken', 'alert_type': 'warning'})
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=email):
                return JsonResponse({'message': 'Email is taken', 'alert_type': 'warning'})
        except User.DoesNotExist:
            pass

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        return JsonResponse({'message': 'User is created. Please login', 'alert_type': 'success'})

    context = {}
    return render(request, "myApp/register.html", context)




def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        myuser=authenticate(username=username, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success (request, "Login Successful")
            return redirect('http://127.0.0.1:8000/home/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('http://127.0.0.1:8000/loginpage/')
    context={}
    return render(request, "myApp/loginpage.html",context)
    


def navigation_bar(request):
    context={}
    return render(request, "myApp/navigation_bar.html")
    

def about(request):
    context={}
    return render(request, "myApp/about.html")


def services(request):
    context={}
    return render(request, "myApp/services.html")


def contact(request):
    context={}
    return render(request, "myApp/contact.html")


def notification(request):
    context={}
    return render(request, "myApp/notification.html")


def home(request):
    context={}
    return render(request, "myApp/home.html")


def emergency(request):
    context={}
    return render(request, "myApp/emergency.html")

def report(request):
    if request.method == 'POST':
        description = request.POST.get('message')
        timestamp = request.POST.get('Time-Stamp')  # Ensure this is properly formatted as a datetime.
        area_code = request.POST.get('Area Code')
        crime_type_name = request.POST.get('Crime Type')
        anonymity_status = request.POST.get('Anonymity Status') == 'on'

        try:
            location = Location.objects.get(area_code=area_code)
        except Location.DoesNotExist:
            return JsonResponse({'message': 'Invalid Area Code', 'alert_type': 'danger'})

        try:
            crime_type = CrimeType.objects.get(name=crime_type_name)
        except CrimeType.DoesNotExist:
            return JsonResponse({'message': 'Invalid Crime Type', 'alert_type': 'danger'})

        incident = IncidentReport(description=description, timestamp=timestamp, anonymity_status=anonymity_status, location=location, crime_type=crime_type)
        incident.save()

        return JsonResponse({'message': 'Incident Report saved successfully', 'alert_type': 'success'})
    return render(request, "myApp/report.html")