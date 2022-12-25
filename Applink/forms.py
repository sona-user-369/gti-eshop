from django import forms
from django.forms import ModelForm
from home.models import *

class RegisterForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}), label='Prénom')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nom')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'minlength':'12'}), label='Mot de passe')
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone')
    class Meta :
        model = Utilisateurs
        fields = ('first_name','last_name', 'email','password', 'contact')

class LoginForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id':'id__email'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id__password'}), label='Mot de passe')
    class Meta:
        model=Utilisateurs
        fields = ('email', 'password')

class UpdateForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Prénom')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nom')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone')
    class Meta :
        model = Utilisateurs
        fields = ('first_name','last_name', 'email', 'contact')

class ChangeForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password1'}), label='Ancien mot de passe')
    Newpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password2'}), label='Nouveau mot de passe')
    Confpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password3'}), label='Confirmation')
    class Meta:
        model = Utilisateurs
        fields =('password',)


class ForgotForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id__password1'}), label='Nouveau mot de passe')
    Confpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id__password2'}), label='Confirmation')
    class Meta:
        model = Utilisateurs
        fields = ('password',)


class ShipForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Prénom')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nom')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Address')
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Ville')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_phone_number'}), label='Phone')

    class Meta:
        model = Livraison
        fields = ('first_name', 'last_name', 'address', 'city', 'phone_number',)

class ReviewForm(ModelForm):
    contenu = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 4}), label='Commentaire*')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nom')

    class Meta:
        model = Avis
        fields =('contenu', 'name',)

class ContactForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nom')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone')
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Sujet')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 4}), label='Message')

    class Meta:
        model = Contact
        fields =('name','email', 'phone', 'subject', 'message')