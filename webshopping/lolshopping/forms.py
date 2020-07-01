from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm
import os

from .models import Account, Customer

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        instance = super(RegistrationForm,self).save(commit=False)
        instance.new_salt = os.urandom(5)
        if commit:
            instance.save()
        return instance

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

class UserProfileForm(ModelForm):
    address_line_2 = forms.CharField(required=False)
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','name','email']
