from django.forms import ModelForm, modelformset_factory
from webstore.models import User, Product, Supplier, Contains, Order
from django import forms


class LoginForm(forms.Form):
	#class Meta:
	#	model = User
	#	fields = ['user_name','user_password']
		#labels = {
		#	'user_name': ('Username'),
		#	'user_password': ('Password'),
		#}
	username = forms.CharField(label='Username',min_length=8,max_length=100)
 	password = forms.CharField(label='Password',widget=forms.PasswordInput())

class RegisterForm(forms.Form):
	# Creation of meta class for Model Form enables direct validation of new entities into User table
	#lass Meta:
	#	model = User
	#	fields = ['user_name','user_email']
	#	labels = {
	#		'user_name': ('Username'),
	#		'user_email': ('Email'),
	#	}
	username = forms.CharField(label='Username',min_length=8,max_length=100)
	password = forms.CharField(min_length=8,widget=forms.PasswordInput())
	repassword = forms.CharField(label='RePassword',min_length=8,widget=forms.PasswordInput())
	email = forms.CharField(label='Email',max_length = 100)
	address = forms.CharField(label='Address',max_length = 100)

ACTIONS = (
	('1','Update Account Information'),
	('2','Delete User Account'),
	('3','View Orders'),
)

class AccountActionForm(forms.Form):
	action = forms.ChoiceField(choices = ACTIONS, required = True)

class AccountUpdateForm(forms.Form):
	password = forms.CharField(min_length=8,widget=forms.PasswordInput())
	repassword = forms.CharField(label='RePassword',min_length=8,widget=forms.PasswordInput())
	email = forms.CharField(label='Email',max_length = 100)
	address = forms.CharField(label='Address',max_length = 100)
	
class AccountDeleteForm(forms.Form):
	confirm = forms.TextInput(attrs={'placeholder':'Enter your email to confirm'})
		