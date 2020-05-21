from django import forms
from django.core.validators import RegexValidator

password_pattern = RegexValidator(regex=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{6,}$',message="Must contain at least uppercase character,lowercase character and special character.")

class LoginForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",error_messages={'required':'Please Enter the Password!'})

class SignupForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",validators=[password_pattern],error_messages={'required':'Please Enter the Password!','min_length':'Password should contain at least 6 characters.'})
    rePassword = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Re Enter Password'}), label="Re Enter Password")
