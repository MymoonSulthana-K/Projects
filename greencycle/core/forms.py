from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter your address")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "address")

from django import forms

class CompostExchangeForm(forms.Form):
    pickup_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    compost_amount = forms.FloatField(min_value=0.5)
