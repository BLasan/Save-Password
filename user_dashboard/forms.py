from django import forms
from django.core.validators import RegexValidator

password_pattern = RegexValidator(regex=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{6,}$',message="Must contain at least uppercase character,lowercase character and special character.")

class ChangeCredentialsForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",error_messages={'required':'Please Enter the Password!'})

class ProfileDataForm(forms.Form):
    user_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'placehoder': 'User Name'}))
    timer = forms.CharField(help_text="Enter the value for auto refreshing timer!", disabled=True, widget=forms.NumberInput(attrs={'value': 10}))

class FeedBackForm(forms.Form):
    reason = forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder': 'Enter Reason for deleting'}),label="Reason",error_messages={'required': 'Please provide the reason for deleting!'})

class LoginForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",error_messages={'required':'Please Enter the Password!'})
