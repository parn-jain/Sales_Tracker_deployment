import datetime
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
import smtplib
from django.contrib import messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from .models import Profile
from django.http import JsonResponse
from django.utils import timezone

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
                    print("I am hereeeeeeeeeee, in middleware")
                    logout(request)
                    response = redirect('login')  # Redirect to login or another page
        return response
    def heartbeat(request):
        if request.user.is_authenticated:
            # Update last activity time
            request.session['last_activity'] = timezone.now().timestamp()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'}, status=401)





# from django.utils.deprecation import MiddlewareMixin
# from django.utils.timezone import now
# from datetime import timedelta
# import datetime
# from django.utils.deprecation import MiddlewareMixin
# from django.utils.timezone import now
# from datetime import timedelta, datetime
# import time
# from django.utils.deprecation import MiddlewareMixin
# from django.utils.timezone import now, make_aware
# from datetime import timedelta, datetime
# import time
# from django.conf import settings

# class InactivityMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         session_expiry = request.session.get('_session_expiry')
        
#         # Convert session_expiry to datetime if it's an int
#         if isinstance(session_expiry, int):
#             session_expiry = datetime.fromtimestamp(session_expiry)
#             # Make session_expiry timezone-aware if using timezones
#             if settings.USE_TZ:
#                 session_expiry = make_aware(session_expiry)
        
#         # Check if the session has expired
#         if session_expiry and now() > session_expiry:
#             request.session.flush()
#         else:
#             # Normal session expiry after 15 minutes
#             expiry_time = now() + timedelta(minutes=15)
#             request.session['_session_expiry'] = time.mktime(expiry_time.timetuple())
        
#         # Keep the session alive if the heartbeat request is made
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'heartbeat' in request.path:
#             request.session.modified = True
#             # Extend the session expiry by 1 hour if the heartbeat is detected
#             expiry_time = now() + timedelta(hours=1)
#             request.session['_session_expiry'] = time.mktime(expiry_time.timetuple())
        
#         return None

#     def process_response(self, request, response):
#         if hasattr(request, 'session') and request.session.modified:
#             # Set the session to expire after 15 minutes (normal session expiry)
#             request.session.set_expiry(15 * 60)
#         return response