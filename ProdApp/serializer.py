from django.db.models.fields.files import ImageFieldFile

from home.models import *

from rest_framework import serializers



class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ("nom","image1", "date_de_stock", "description_courte", "description_longue", "stock", "prix", "categorie", 'sous_categorie')




class ProduitSerializer_ext(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ("nom","image1", "date_de_stock", "description_courte", "description_longue" , "stock", "prix", "categorie", 'sous_categorie')


    def validate_nom(self, data):
        get_nom_product = Produit.objects.filter(nom=data)
        if len(get_nom_product) != 0:
            raise serializers.ValidationError('Cet produit existe deja')

        return data

class LivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livraison
        fields = ('first_name', 'last_name', 'address', 'city', 'phone_number')

    def validate_phone_number(self,value):
        try:
            verify = int(value)
        except:
            verify = None

        if verify is None:
            raise serializers.ValidationError("Le numero de telephone est incorrect")

        return value

    def perform_save(self, validated_data):
        object_livraison, _ = Livraison.objects.get_or_create(first_name= validated_data["first_name"],
                                                 last_name = validated_data["last_name"],
                                                 address = validated_data["address"],
                                                 city = validated_data["city"],
                                                 phone_number = validated_data["phone_number"])


        object_livraison.save()
        return object_livraison

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields =('contenu', 'name')

class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = ('nom',)


class CategorieSerializer_ext(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = '__all__'

    def validate_nom(self, data):
        get_nom_categorie = Categorie.objects.filter(nom=data)
        if len(get_nom_categorie) !=0 :
            raise serializers.ValidationError('Cet categorie existe deja')

        return data


class SousCategorieSerializer_ext(serializers.ModelSerializer):
    class Meta :
        model = SousCategorie
        fields = '__all__'





class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta :
        model = SousCategorie
        fields = '__all__'

    def validate_nom(self, data):
        get_nom_sous_categorie = SousCategorie.objects.filter(nom=data)
        if len(get_nom_sous_categorie) != 0:
            raise serializers.ValidationError('Cet sous-categorie existe deja')

        return data

    def perform_save(self, validated_data):

        sous_categorie_created = SousCategorie.objects.create(nom=validated_data['nom'], categorie= validated_data['categorie'])
        sous_categorie_created.save()

        return sous_categorie_created


class ShowReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields = '__all__'


class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commandes
        fields = '__all__'