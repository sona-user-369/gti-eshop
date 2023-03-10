from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteInplaceWidget , SummernoteWidget
from django_summernote.fields import SummernoteTextField
from home.models import *


class ProduitForm(ModelForm):
    image1 = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image2 = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image3 = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description_courte = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    description_longue = forms.CharField(widget=SummernoteWidget(attrs={'class': 'form-control', 'summernote': {'width':'100%', 'height':'480px'}}), required=False)
    additional_info = forms.CharField(widget=SummernoteWidget(attrs={'class': 'form-control', 'summernote': {'width':'100%', 'height':'480px'}}),label='Information additionnel')
    prix = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    categorie = forms.ModelChoiceField( queryset=Categorie.objects.all(),  widget=forms.Select(attrs={'class': 'form-control'}))
    sous_categorie = forms.ModelChoiceField(queryset=SousCategorie.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    brand = forms.ModelChoiceField(queryset=Mark.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Produit
        fields = ['image1',
                  'image2',
                  'image3',
                  'nom',
                  'stock',
                  'description_courte',
                  'description_longue',
                  'additional_info',
                  'prix',
                  'categorie',
                  'sous_categorie',
                  'brand',]
        # widgets = {
        #     'description_longue': SummernoteInplaceWidget(attrs={'class': 'form-control'})
        # }

class CategorieForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=True,)
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Categorie
        fields = '__all__'

class SousCategorieForm(ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = SousCategorie
        fields = '__all__'