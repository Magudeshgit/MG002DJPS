from django import forms
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from .models import Users

class RegisterForm(UserCreationForm):
	class Meta:
		model = Users
		fields = ["business_name","email","password1", "password2"]
class LoginForm(AuthenticationForm):
	class Meta:
		model = Users
		fields = ["username", "password1"]