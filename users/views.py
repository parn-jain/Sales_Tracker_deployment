from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm, LoginForm, CallingDetailsForm
from .models import Profile, CallingDetail, AttendanceRecord
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from sales_tracker.requirements import timer, send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from sales_tracker.models import MiningData
import pytz #used to set our required time zone
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.utils import timezone
import datetime
from sales_tracker.analysis import generate_bar_chart, TotalDays
from sales_tracker.admin_analysis import admin_attendence_graph

# MY CODE 

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Welcome {username}, your account is created")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form" : form})

# class ProfileView(CreateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = "users/profile.html"

def index(request):
    return render(request, 'users/index.html')

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        username = request.user.username

        profile_detail = Profile(user = get_user_model().objects.get(username=username), emp_id = form.data.get("emp_id"), dob = form.data.get("dob"), branch = form.data.get("branch"))
        profile_detail.save()
        return redirect("index")
    else:
        form = ProfileForm()
    return render(request, "users/profile.html", {"form":form})


@login_required
def detail_profile(request):
    try:
        user_ = get_user_model().objects.get(username=request.user.username)
        user_info = Profile.objects.get(user = user_)
        return render(request, "users/profile_detail.html", {"user_info":user_info, "user": user_})
    except:
        return redirect("profile")
    
    

def forget_pass(request):
    if request.method == "POST":
        form = request.POST
        email = form["e-mail"]

        return redirect("profile")
    else:
        return render(request, "users/forgetpassword.html")




class LogoutView(TemplateView):
    template_name = "users/logout.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        elapsed_time_in_sec = int(elapsed_time[0])*60*60 + int(elapsed_time[1])*60 + int(elapsed_time[2])
        if elapsed_time_in_sec < 28_000:
            custom_message = "You cannot log out yet."
        else:
            custom_message = "Goodbye!"
        context['custom_message'] = custom_message
        if elapsed_time_in_sec < 28_000:
            send_mail(elapsed_time, user.username)
            user_profile = Profile.objects.get(user = user.id)
            user_profile.can_logout = False
            user_profile.save()
            # pass
        else:
            user_profile.can_logout = True
            # logout(request)
        if(user_profile.can_logout):
            logout(request)
        else:
            return context
        return context
    


def Reason(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    elapsed_time_in_sec = int(elapsed_time[0])*60*60 + int(elapsed_time[1])*60 + int(elapsed_time[2])
    if request.method == "POST":
        current_datetime = timezone.localtime()
        current_time = current_datetime.strftime('%H:%M:%S')
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        print("Current Time:", current_time)
        existing_record = AttendanceRecord.objects.filter(user=user, date=now_date).first()
        if existing_record:
            # Update the check_out_time with the current time
            existing_record.check_out_time = current_time
            existing_record.save()
        reason = request.POST.get("reason_form")
        password = "axzf ekbv uawt rugt"
        print("check")
        print(user)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'pjisvgreat@gmail.com'
        receiver_email = user.email
        subject = "AAPAI"
        full_message = f"{elapsed_time}, {reason}"
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(full_message, 'html'))      
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  
            server.login(sender_email, password)  
            text = message.as_string()  
            server.sendmail(sender_email, receiver_email, text)
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")
        finally:
            server.quit()
        user_profile = Profile.objects.get(user = user.id)
        user_profile.can_logout = False
        user_profile.save()
        logout(request)
        return redirect("login")



def Mining_ct(user):
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date, assigned_to = user)
    today_mining_count = today_mining.count()
    return today_mining_count
    
def Logout(request):
    context = {}
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    elapsed_time_in_sec = int(elapsed_time[0])*60*60 + int(elapsed_time[1])*60 + int(elapsed_time[2])
    if elapsed_time_in_sec < 70: 
        return render(request, 'users/reason.html')
    else:
        mining_count = Mining_ct(user)
        if mining_count >= 2:
            # user_profile.can_logout = True
            # user_profile.save()
            logout(request)
            return render(request, 'users/logout.html', {'message': 'Successfully logged out.'})
        else:
            # messages.warning(request, "You need to complete at least 40 mining tasks before logging out.")
            return render(request, 'users/reason.html')

    
     
from django.contrib.auth import authenticate, login
    
def manual_login(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Implement secure user authentication logic using username and password
            # ...
            user = authenticate(request, email = email, password = password)
            print("this is userrrrrrrr" ,user)


            if user is not None:
                # User is authenticated, proceed with login logic...
                try:
                    user_profile = Profile.objects.get(user = user)
                except:
                    login(request, user)
                    return redirect("profile")
                if user_profile.can_login:
                    login(request, user)
                    generate_bar_chart(request)
                    admin_attendence_graph()
                    # print(timezone.now().time())
                    current_date = timezone.now().date()
                    Nuser = request.user.id
                    current_datetime = timezone.now()
                    current_date = current_datetime.date()
                    current_time = current_datetime.time()
                    now = datetime.datetime.now()
                    # print("Current Time:", now.time())
                    current_datetime = timezone.localtime()
                    current_time = current_datetime.strftime('%H:%M:%S')
                    print("Current Time:", current_time)
                    existing_record = AttendanceRecord.objects.filter(user=user, date=current_date).first()
                    if not existing_record:
                        AttendanceRecord.objects.create(
                            user=user,
                            date=current_date,
                            check_in_time=current_time,
                            status='Present'
                        )
                    print("Nusewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwr")
                    print(Nuser)
                    if user_profile.branch == "admin":
                        
                        return redirect("adminn")
                    elif user_profile.branch == "miner":
                        return redirect("index")
                    elif user_profile.branch == "agent":
                        return redirect("agent")

                else:
                    error_message = 'Your access is denied, Please contact Admin for access'
                    return render(request, 'users/login.html', {'form': form, 'error_message': error_message})
                # return redirect("index")
            else:
                error_message = 'Invalid username or password.'
        else:
            error_message = 'Please correct the errors below.'  # Handle form validation errors
    else:
        form = LoginForm()
        error_message = None

    return render(request, 'users/login.html', {'form': form, 'error_message': error_message})

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

# from django.views.generic.edit import CreateView


# class CallingDetailsView(CreateView):
#     model = CallingDetail
#     form_class = CallingDetailsForm
#     template_name = "sales_tracker/calling_details.html"
#     success_url = "videocall"


def calling_details_view(request):
    if request.method == "POST":
        form = CallingDetailsForm(request.POST)
        username = request.user.username
        try:
            is_already_there = CallingDetail.objects.get(customer_email = form.data.get("customer_email"))
            print(is_already_there)
        except:
            calling_details = CallingDetail(caller = get_user_model().objects.get(username=username), customer_first_name = form.data.get("customer_first_name"), customer_last_name = form.data.get("customer_last_name"), customer_email = form.data.get("customer_email"), customer_contact_number = form.data.get("customer_contact_number"), customer_address = form.data.get("customer_address"))
            calling_details.save()
        return redirect("videocall")    
    else:
        form = CallingDetailsForm()
    return render(request, "users/calling_details.html", {"form":form})



@login_required
def some_view(request):
    user = request.user
    password = "axzf ekbv uawt rugt"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'pjisvgreat@gmail.com'
    receiver_email = user.email
    subject = "AAPAI"
    full_message = f"{user} was idle for 15 mins"
    message = MIMEMultipart()
    print("This is sending mail")
    message['From'] = sender_email
    message['To'] = receiver_email  
    message['Subject'] = subject
    message.attach(MIMEText(full_message, 'html'))      
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(sender_email, password)  
        text = message.as_string()  
        server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        messages.error(request, f"Error sending email: {e}")
    finally:
        server.quit()
    return render(request, 'users/login.html')