from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

from django.utils import timezone



# Create your models here.

class RegisterUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('miner', 'Data Miner'),
        ('agent', 'Calling Agent'),
    )
    user = models.OneToOneField(RegisterUser, on_delete=models.CASCADE, default= get_user_model(), primary_key=True)
    emp_id = models.CharField(max_length=50,default="qw")
    dob = models.DateField()
    branch = models.CharField(max_length=10, choices=USER_ROLES)
    can_login = models.BooleanField(default=True)
    can_logout = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
    

class AttendanceRecord(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')],
        default='Present'  # Default to 'Absent' for existing records
    )

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.status}"






    
class CallingDetail(models.Model):
    caller = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default= get_user_model())
    customer_first_name = models.CharField(max_length=50, default="")
    customer_last_name = models.CharField(max_length=50, default= "")
    customer_email = models.EmailField(default="@gmail.com", unique=True)
    customer_contact_number = models.IntegerField(default=91)
    customer_address = models.TextField(default="")
