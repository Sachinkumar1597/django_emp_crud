from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Records
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput

# Register user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']


# login user
class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput())
    password=forms.CharField(widget=PasswordInput)


# Create Record
class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = ['first_name','last_name','phone_no','email','address','city','country']



# Update Record
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = ['first_name','last_name','phone_no','email','address','city','country']