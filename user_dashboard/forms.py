from django import forms
from django.core.validators import RegexValidator

password_pattern = RegexValidator(regex=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{6,}$',message="Must contain at least uppercase character,lowercase character and special character.")

class ChangeCredentialsForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",error_messages={'required':'Please Enter the Password!'})
