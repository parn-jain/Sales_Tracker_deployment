import datetime
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
import smtplib
from django.contrib import messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from .models import Profile

class InactivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Update the last activity timestamp for the user
            request.session['last_activity'] = datetime.datetime.now().timestamp()
    
    def process_response(self, request, response):
        user = request.user
        if request.user.is_authenticated:
            # Check for inactivity and expire session if needed
            last_activity = request.session.get('last_activity')
            if last_activity:
                current_time = datetime.datetime.now().timestamp()
                if (current_time - last_activity) > (15 * 60):  # 15 minutes
                    from django.contrib.auth import logout
                    print("I am hereeeeeeeeeee")
                    logout(request)
                    response = redirect('login')  # Redirect to login or another page
        return response
