from home.models import *
from django import forms
from rest_framework import serializers
from django.contrib.auth.hashers import check_password


class GoogleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('first_name', 'last_name', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = "__all__"
        excludes = ('username',)


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('first_name', 'last_name', 'email', 'contact')

    def validate_contact(self, data):
        try:
            int(data)
            convert_contact = 1
        except:
            convert_contact = 0

        if not convert_contact:
            raise serializers.ValidationError("Entrer un contact valide")

        return data


class FillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('first_name', 'last_name', 'email', 'password', 'contact')

    def validate_contact(self, data):
        try:
            int(data)
            convert_contact = 1
        except:
            convert_contact = 0

        if not convert_contact:
            raise serializers.ValidationError("Entrer un contact valide")

        return data


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('email',)

    def validate_email(self, data):
        contain_email = Utilisateurs.objects.filter(email=data)
        if len(contain_email) != 1:
            raise serializers.ValidationError("L'email entre néxiste pas")
        return data


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('email',)


class ChangeSerializer(serializers.Serializer):
    password = serializers.CharField()
    Newpassword = serializers.CharField()
    Confpassword = serializers.CharField()


class ForgotSerializer(serializers.Serializer):
    password = serializers.CharField()
    confpassword = serializers.CharField()

    def validate(self, data):
        new = data["password"]
        conf = data["confpassword"]

        if new != conf:
            return serializers.ValidationError("Les mots de passe ne se correspondent pas")

        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('first_name', 'last_name', 'email', 'password', 'contact')

    def validate_contact(self, data):
        try:
            int(data)
            convert_contact = 1
        except:
            convert_contact = 0

        if not convert_contact:
            raise serializers.ValidationError("Entrer un contact valide")

        return data

    def validate_email(self, data):
        contain_email = Utilisateurs.objects.filter(email=data)
        if len(contain_email) == 1:
            raise serializers.ValidationError("Cet email existe deja")
        return data


class UserLoginSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = ('email', 'password')

    def validate_email(self, data):
        global contain_email
        contain_email = Utilisateurs.objects.filter(email=data)

        if len(contain_email) != 1:
            raise serializers.ValidationError("Le mot de passe ou l'email est incorrect")
        else:
            for user in contain_email:
                if user.is_active == 0:
                    raise serializers.ValidationError("Le mot de passe ou l'email est incorrect")

        return data

    def validate_password(self, data):
        if len(contain_email) != 1:
            raise serializers.ValidationError("Le mot de passe ou l'email est incorrect")
        else:
            user = contain_email
        if user is not None:
            for util in user:

                if not check_password(data, str(util.password)) and util.password != data:
                    raise serializers.ValidationError("Le mot de passe ou l'email est incorrect")

        return data


class ContactSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject', 'message')

    def validate_phone(self, data):
        try:
            int(data)
            convert_contact = 1
        except:
            convert_contact = 0

        if not convert_contact:
            raise serializers.ValidationError("Entrer un contact valide")

        return data
