from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, CallingDetail

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    # dob = forms.DateField()
    # branch = forms.CharField()

    class Meta:
        model = User
        fields = [ "username", "email", "password1", "password2",]
        


class ProfileForm(forms.ModelForm):
    emp_id = forms.CharField(label = 'Employee ID')
    dob = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}), label = 'Date of birth')
    class Meta:
        model = Profile 
        fields = ['emp_id','dob','branch']


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

        

class CallingDetailsForm(forms.ModelForm):
    class Meta:
        model = CallingDetail
        fields = "__all__"
        exclude = ["caller"]
        
