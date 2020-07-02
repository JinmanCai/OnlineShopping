from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
import os

from .models import Account, Customer

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

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

class UserProfileForm(ModelForm):
    address_line_2 = forms.CharField(required=False)
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','name','email']
