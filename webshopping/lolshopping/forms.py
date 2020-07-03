from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
import os
import hashlib

from .models import Account, Customer

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address',)
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
        raw_password = self.cleaned_data.get('password1')
        salt = os.urandom(5)
        instance.new_salt = str(salt)
        new_hash_val = hashlib.pbkdf2_hmac('sha256', raw_password.encode(), str.encode(instance.new_salt), 100000)
        instance.new_hash_value = new_hash_val.hex()



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
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                raise forms.ValidationError("Invalid login")
            # if not authenticate(email=email):
            #     print(email)
            #     raise forms.ValidationError("Invalid login")


class UserProfileForm(ModelForm):
    address_line_2 = forms.CharField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','name','email']
