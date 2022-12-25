from home.models import *

from django.forms import ModelForm
from django import forms
class UserFormRegister(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput)
