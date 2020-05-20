from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",error_messages={'required':'Please Enter the Password!'})

class SignupForm(forms.Form):
    email = forms.EmailField(required=True,help_text='abcd@gmail.com',widget=forms.EmailInput(attrs={'placeholder':'Email'}),label="Email",error_messages={'required':'Please Enter the Email!'})
    password = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label="Password",error_messages={'required':'Please Enter the Password!'})
    rePassword = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Re Enter Password'}), label="Re Enter Password")

