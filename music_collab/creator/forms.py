from django import forms
from django.contrib.auth.models import User

class CreatorRegistrationForm(forms.ModelForm):
    password=forms.CharField(label="password",widget=forms.PasswordInput)
    cpassword=forms.CharField(label="confirm password",widget=forms.PasswordInput)
    email=forms.EmailField(required=True)
    phone=forms.IntegerField(label='phone',widget=forms.TextInput(attrs={'placeholder':'enter your phone number'}))
    class Meta:
        model =User
        fields=['username','first_name','last_name','email','phone','password','cpassword']