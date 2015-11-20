from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='Username',max_length=100)
 	password = forms.CharField(label='Password',widget=forms.PasswordInput())

class RegisterForm(forms.Form):
	username = forms.CharField(label='Username',max_length=100)
	password = forms.CharField(widget=forms.PasswordInput())
	repassword = forms.CharField(label='Re-Password',widget=forms.PasswordInput())
	email = forms.CharField(label='Email',max_length = 100)
	address = forms.CharField(label='Address',max_length = 100)


