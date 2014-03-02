from django import forms
from report.models import Client
from django.contrib.auth.models import User

class ClientForm(forms.ModelForm):
    clientname = forms.CharField(max_length = 128, help_text="Please enter the client name.")
    clientemail = forms.EmailField(max_length = 50, help_text="Please enter the client email.")
    dataiumclientid = forms.IntegerField(initial=0)
    dataiumreportmonth = forms.CharField(max_length=50)
    clienthasoptedout = forms.CharField(max_length=3, help_text="Enter YES if client has opted-out of market report")
    clientdma = forms.CharField(max_length=50)
    clientcity = forms.CharField(max_length=50)
    clientstate = forms.CharField(max_length=12)
    clientwebsite = forms.CharField(max_length=50)
    clientshopimage = forms.CharField(max_length=100)
    clientdmmimage = forms.CharField(max_length=100)
    clienthitlistimage = forms.CharField(max_length=100)
    clientsocialimage = forms.CharField(max_length=100)
    clientutilityimage = forms.CharField(max_length=100)
    
    class Meta:
        model = Client
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username','email','password')
        