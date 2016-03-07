from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from webshop.models import UserProfile


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=255, required=True, label="first name")
	last_name= forms.CharField(max_length=255, required=True, label="last name")
	email = forms.EmailField(required=True, label = "Email")
	is_dev= forms.BooleanField(required=False, label="is_dev")
	password1= forms.CharField(required=True, label='enter password')
	password2= forms.CharField(required=True, label='enter password again')

	class Meta:
		model = User
		fields = ("first_name","last_name", "username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=True)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user_profile = UserProfile(user=user, is_dev=self.cleaned_data['is_dev'])
		#user_profile.save()
		#user_profile.email = self.cleaned_data["email"]
		#user_profile.username = self.cleaned_data["username"]
		#user_profile.password = self.cleaned_data["password1"]
		user_profile.is_dev = self.cleaned_data["is_dev"]
		#user_profile.save()
		if user_profile.is_dev:
			user.groups.add(Group.objects.get(name='Developers'))
		if commit:
			user.save()
			user_profile.save()
		return user, user_profile

