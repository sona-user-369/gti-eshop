from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
class Utilisateurs(AbstractUser):

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    #REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password',  'contact']
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    contact = models.CharField(max_length=50, null=False, blank=False)
    is_active = models.BooleanField(default=0)
    class Meta :
        verbose_name ="Utliisateur"

    def __str__(self):
        return self.last_name


class Categorie(models.Model):
    image = models.ImageField(null=True)
    nom = models.CharField(max_length=50, null=False, blank=False)

    class Meta :
        verbose_name = "Categorie"

    def __str__(self):
        return self.nom

class SousCategorie(models.Model):
    nom = models.CharField(max_length=50, null=False, blank=False )
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta :
        verbose_name = "Sous-Categorie"

    def __str__(self):
        return self.nom

class Livraison(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    last_name = models.CharField(max_length=50,null=False, blank=False, default=None)
    address = models.CharField(max_length=50, null=False, blank=False, default=None)
    city = models.CharField(max_length=50, null=False, blank=False, default=None)
    phone_number = models.CharField(max_length=20, null=False, blank=False, default=None)

    class Meta:
        verbose_name = "Livraison"

    def __str__(self):
        return self.address


class Commandes(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False , default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(null=False, blank=False, default=timezone.now())
    livree = models.BooleanField(null=False, blank=False, default=0)
    valide = models.BooleanField(null=False, blank=True, default=0)
    pending = models.BooleanField(null=False, blank=False, default=1)
    livraison = models.ForeignKey(Livraison, on_delete=models.PROTECT , null=True)
    date_livraison = models.DateTimeField(null=True, blank=True, default=None,)
    prix_total = models.PositiveIntegerField(null=False, blank=False,default=0)
    ship_option = models.CharField(null=True,blank=False, max_length=20)

    class Meta :
        verbose_name = "Commande"

    def __str__(self):
        return self.utilisateur




class Panier(models.Model):
    id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Panier"


class Favoris(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)

    class Meta :
        verbose_name = "Favori"


class Mark(models.Model):
    id = models.UUIDField(primary_key=True)
    nom = models.CharField(max_length=100, blank=False, null=False)

    class Meta :
        verbose_name = "Marque"


class Produit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image1 = models.ImageField(null=True)
    image2 = models.ImageField(null=True)
    image3 = models.ImageField(null=True)
    nom= models.CharField(max_length=100, null=False, blank=False)
    date_de_stock = models.DateTimeField(null=False, blank=False, default=timezone.now())
    stock = models.PositiveIntegerField(null=False, blank=False)
    description_courte = models.TextField(max_length=500, null=True, blank=False)
    description_longue = models.TextField(max_length=500, null=True, blank=False)
    prix = models.PositiveIntegerField(null=False , blank=False)
    categorie = models.ForeignKey(Categorie,  on_delete=models.PROTECT)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.PROTECT, default=None, null=True, blank=False)
    brand = models.ForeignKey(Mark, on_delete=models.PROTECT , default="", null=True)
    panier = models.ManyToManyField(Panier, through="PanierProduit")
    favoris = models.ManyToManyField(Favoris)
    commande = models.ManyToManyField(Commandes, through="CommandeProduit")
    qr_code_file = models.ImageField(null=True)
    is_archive = models.BooleanField(null=False, blank=False, default=False)


    class Meta :
        verbose_name = "Produit"

    def __str__(self):
        return self.nom

class PanierProduit(models.Model):
    product = models.ForeignKey(Produit, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(null=False, blank=False, default=1)


class CommandeProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    commande = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(null=False, blank=False, default=1)



class Image(models.Model):
    title = models.CharField(blank=True, max_length=100)
    flickr_id = models.IntegerField(default=0)
    source = models.CharField(max_length=50)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.source)

    class Meta:
        verbose_name="Photo de produit"


class Avis(models.Model):
    utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    name= models.CharField(max_length=20, null=False, blank=False , default='')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    contenu = models.TextField(max_length=500, null=False , blank= False)
    date = models.DateTimeField(null=False, blank=False, default=timezone.now())
    rating = models.IntegerField(default=0)
    class Meta :
        verbose_name = "Avis"

    def __str__(self):
        return self.contenu




class Facture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    commande = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(null=False, blank=False, default=0)
    source = models.FileField(null=True, upload_to='invoices')

    class Meta :
        verbose_name = "Facture"

    def __str__(self):
        return self.utilisateur

class Contact(models.Model):
    name = models.CharField(max_length=30, null=False, default='')
    email = models.EmailField(null=False, default='a@a')
    phone = models.CharField(max_length=45, null=False , default='')
    subject = models.CharField(max_length=10, null=False, default='')
    message = models.TextField(max_length=200, null=False, default='')
    create_at = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name = 'Contacts'

    def __str__(self):
        return self.name






