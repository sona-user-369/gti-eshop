import os

import requests
from authy.api import AuthyApiClient
from django.shortcuts import render, HttpResponse
from rest_framework import exceptions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.authentication import authenticate, TokenAuthentication
from django.utils.translation import gettext
from django.utils import translation

from EShopGTI import settings
from EShopGTI.settings import SITE_HOSTNAME
from ProdApp.serializer import ProduitSerializer
from .serializer import *
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from home.models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from home.forms import *
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from .auth import ExpiringTokenAuthentication
import json
from django.utils import timezone
import uuid
from home.Manage import verify_user, subscribe, ExtendedEncoder, ExtendedDecoder
from twilio.rest import Client

# authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)
verify_sid = "VA93ae23c69e697c1496b94e13e96293b7"
client = Client(settings.ACCOUNT_SID, settings.ACCOUNT_SECURITY_API_KEY)


# Register User of App
@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':

        a = request.data['data'].split('&')
        liste = []
        for i in range(1, 6):
            b = a[i].split('=')
            liste.append(b[1])
        # print(liste)
        format_email = liste[2].replace('%40', '@')
        print(format_email)
        data_got = {'first_name': liste[0],
                    'last_name': liste[1],
                    'email': format_email,
                    'password': liste[3],
                    'contact': request.data['dial-code'] + liste[4],
                    }
        RegisterSerialiser = UserRegisterSerializer(data=data_got)
        if RegisterSerialiser.is_valid():
            RegisterSerialiser.validated_data["password"] = make_password(
                RegisterSerialiser.validated_data.get("password"))
            user = RegisterSerialiser.save()
            print(RegisterSerialiser.data)
            if request.data['superuser'] == 1:
                user.__dict__.update({'is_superuser': 1, 'is_active': 1})
                user.save()
            else:
                if request.data['add'] == 1:
                    pass
                else:
                    current_site = get_current_site(request)
                    message = render_to_string(
                        "Applink/EmailConfirmation.html",
                        {
                            "user": user,
                            "domain": current_site,
                            "token": PasswordResetTokenGenerator().make_token(user),
                            "uid": urlsafe_base64_encode(user.pk.bytes)
                        }
                    )

                    email = RegisterSerialiser.validated_data.get('email')

                    mail_subject = "Confirmation d'email"

                    mail = EmailMessage(mail_subject, message, to=[email])

                    mail.send()

            return Response(RegisterSerialiser.data, status=200)
        else:
            return Response(RegisterSerialiser.errors, status=400)


    else:
        RegisterSerialiser = UserRegisterSerializer()

    return Response(RegisterSerialiser)


def serialize_uuid(uuid_object, cls=json.JSONEncoder):
    return cls().encode(uuid_object)


# Login User of App
@api_view(['POST'])
def loginUser(request):
    if request.method == 'POST':

        try:
            from_google = request.data['from_google']
        except:
            from_google = None

        if from_google is None:

            a = request.data['data'].split('&')
            liste = []
            for i in range(1, 3):
                b = a[i].split('=')
                liste.append(b[1])

            format_email = liste[0].replace('%40', '@')
            print(format_email)
            data_got = {

                'email': format_email,
                'password': liste[1],

            }
        else:
            data_got = request.data
            format_email = request.data['email']
        can_login = 0
        print(data_got)
        LoginSerializer = UserLoginSerialiser(data=data_got)
        if LoginSerializer.is_valid():
            user = Utilisateurs.objects.get(email=format_email)
            if int(request.data['verify_superuser']) == 1:
                print(user.is_superuser)
                if user.is_active:

                    if user.is_superuser:
                        verification = client.verify.v2.services(verify_sid) \
                            .verifications \
                            .create(to='+22952623705', channel="sms")

                        print(verification.status)

                        request.session['first_tent'] = 1
                        request.session['phone_number'] = '+22952623705'
                        request.session['email'] = user.email
                        contact_crypt = str('+22952623705')
                        contact_crypt = list(contact_crypt)
                        print(contact_crypt)
                        for i in range(3, 7):
                            contact_crypt[i] = '*'
                        contact = ''
                        for index in contact_crypt:
                            contact += index

                        return Response({'phone_number': contact}, status=200)
                    else:

                        return Response({'warning': 1}, status=400)
                else:
                    can_login = 0
            else:
                if user.is_active:
                    can_login = 1
                else:
                    can_login = 0

            if can_login:

                user.last_login = timezone.now()
                user.save()
                token, _ = Token.objects.get_or_create(user=user)

                request.session["token"] = model_to_dict(token)["key"]

                primary_key = str(user.pk)
                primary_key = primary_key.replace('-', '')
                print(request.session["token"])
                request.session["user_primary"] = primary_key
                cart, _ = Panier.objects.get_or_create(utilisateur=user)
                wishlist, _ = Favoris.objects.get_or_create(utilisateur=user)
                cart.save()
                wishlist.save()
                requests.get(url="http://" + SITE_HOSTNAME + "/extlink/update_to_cart_object")
                requests.get(url="http://" + SITE_HOSTNAME + "/extlink/update_to_wishlist_object")

                # reponse = {"Login" :LoginSerializer.data, "token": token}

                return Response({"token": model_to_dict(token)["key"]}, status=200)
            else:
                print('Attention')
                return Response(status=400)
        else:
            print(LoginSerializer.errors)
            return Response(LoginSerializer.errors, status=400)


@api_view(['POST'])
def phone_verification(request):
    print('cool')
    if request.session['first_tent'] == 1:
        request.session['first_tent'] = 0
        request.session['tentative'] = 1
    if int(request.session['tentative']) <= 3:
        try:
            verification_check = client.verify.v2.services(verify_sid) \
                .verification_checks \
                .create(to=request.session['phone_number'], code=request.data['otp'])
        except:
            return Response({'expired_code': 1}, status=400)
    else:
        return Response({'expired_code': 1}, status=400)
    request.session['tentative'] = request.session.get('tentative') + 1
    if verification_check.status == 'pending':
        request.session['tentative'] = 1
        return Response({'code_invalid': 1}, status=400)
    else:
        user = Utilisateurs.objects.get(email=request.session.get('email'))
        user.last_login = timezone.now()
        user.save()
        token, _ = Token.objects.get_or_create(user=user)

        request.session["token"] = model_to_dict(token)["key"]

        primary_key = str(user.pk)
        primary_key = primary_key.replace('-', '')
        print(request.session["token"])
        request.session["user_primary"] = primary_key
        cart, _ = Panier.objects.get_or_create(utilisateur=user)
        wishlist, _ = Favoris.objects.get_or_create(utilisateur=user)
        cart.save()
        wishlist.save()
        return Response(status=200)


@csrf_exempt
@api_view(["GET", "PUT", "POST"])
def change_password(request):
    user = Utilisateurs.objects.get(pk=request.session["user_primary"])

    if request.method == 'POST':
        changeSerializer = ChangeSerializer(data=request.data)
        print(request.data)

        if changeSerializer.is_valid():

            print("ooooooooooooooooooooooooooooooooooooooook")
            if check_password(changeSerializer.validated_data["password"], str(user.password)):

                if changeSerializer.validated_data["Newpassword"] == changeSerializer.validated_data["Confpassword"]:

                    changeSerializer.validated_data["Confpassword"] = make_password(
                        changeSerializer.validated_data.get("Confpassword"))
                    user.__dict__update({'password': changeSerializer.validated_data["Confpassword"]})
                    user.save()
                else:
                    return Response({"new": "mot de passe de confirmation invalide"}, status=400)
            else:
                return Response({"old": "l'ancien mot de passe n'est pas correct"}, status=400)

            return Response(changeSerializer.data, status=200)
        else:
            print(changeSerializer.errors)
            return Response(changeSerializer.errors, status=400)


@api_view(['POST'])
def registerUserGoogle(request):
    if request.method == 'POST':
        RegisterSerialiser = FillSerializer(data=request.data)
        if RegisterSerialiser.is_valid():
            RegisterSerialiser.validated_data["password"] = make_password(
                RegisterSerialiser.validated_data.get("password"))
            user = request.session["google"]
            User = Utilisateurs.objects.get(email=user['email'])
            User.__dict__.update(RegisterSerialiser.data)
            User.save()
            User.__dict__.update({'is_active': 1})
            User.save()

            url = "http://" + SITE_HOSTNAME + "/link/login"
            response = requests.post(url, data={'email': user['email'], 'password': request.data['password'],
                                                'from_google': 1, 'verify_superuser': 0})
            request.session['token'] = response.json()['token']
            print(response.json())
            return Response(RegisterSerialiser.data, status=200)
        else:

            return Response(RegisterSerialiser.errors, status=400)


    else:
        RegisterSerialiser = UserRegisterSerializer()

    return Response(RegisterSerialiser)


@csrf_exempt
@api_view(["GET", "DELETE"])
# @authentication_classes([ExpiringTokenAuthentication])
# @permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(key=request.session["token"])
        t = model_to_dict(token)
        # print(t)
        token.delete()
        return Response({"token": "delete"}, status=200)
    except(Token.DoesNotExist):
        return Response({"token": "not delete"}, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "POST"])
def update(request):
    user = Utilisateurs.objects.get(pk=request.session["user_primary"])

    if request.method == 'POST':
        UpdateSerializer = ProfilSerializer(data=request.data)

        if UpdateSerializer.is_valid():

            user.__dict__.update(UpdateSerializer.data)
            user.save()

            return Response(UpdateSerializer.data, status=200)
        else:
            return Response(UpdateSerializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "DELETE"])
# @authentication_classes([ExpiringTokenAuthentication])
# @permission_classes([IsAuthenticated])
def delete(request):
    user = Utilisateurs.objects.get(pk=request.session["user_primary"])
    user.delete()

    return Response({"user": "deleted"}, status=200)


@csrf_exempt
@api_view(["GET"])
@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
def profil(request, id):
    user = Utilisateurs.objects.get(pk=id)
    user_serializer = UserSerializer(data=user)
    return Response(user_serializer, status=200)


@csrf_exempt
@api_view(["POST"])
def subscribtion(request):
    if request.method == 'POST':
        Subscriber = SubscribeSerializer(data=request.data)
        if Subscriber.is_valid():
            subs = subscribe(Subscriber.validated_data['email'])
            print(subs)
            if not subs:
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                return Response(status=400)
            else:
                return Response(status=200)

        else:
            print("issssssssssssssssssssssssssssssssssssss")
            return Response(Subscriber.errors, status=400)


@csrf_exempt
@api_view(["GET"])
@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
def sample_api(request):
    token = model_to_dict(request.auth)["key"]
    cart = Panier.objects.get(utilisateur=request.user)
    wishlist = Favoris.objects.get(utilisateur=request.user)
    cart.save()
    total_cart = len(cart.produit_set.all())
    total_wishlist = len(wishlist.produit_set.all())

    all_produits_cart = cart.produit_set.all()
    product_list_cart = []
    subtotal = 0

    for produit in all_produits_cart:
        model_p = model_to_dict(produit)
        p = ProduitSerializer(data=model_p)
        if p.is_valid():

            quantite_produit = PanierProduit.objects.get(panier=cart, product=produit).quantite
            product_list_cart.append(
                {'produit': {"pk": str(produit.pk), "fields": p.data}, 'quantite': quantite_produit,
                 'total': produit.prix * quantite_produit})

            subtotal += produit.prix * quantite_produit

        else:
            print(p.errors)
            return Response(status=400)
    all_produits_wishlist = wishlist.produit_set.all()

    product_list_wishlist = []
    # print(model_to_dict(request.user))
    for produit in all_produits_wishlist:
        model_p = model_to_dict(produit)

        p = ProduitSerializer(data=model_p)
        if p.is_valid():

            if produit.stock == 0:
                # pr=json.dumps(model_to_dict(produit) , cls=ExtendedEncoder)
                product_list_wishlist.append({"produit": {"pk": str(produit.pk), "fields": p.data}, "in_stock": False})

            else:
                # pr = json.dumps(model_to_dict(produit), cls=ExtendedEncoder)
                product_list_wishlist.append({"produit": {"pk": str(produit.pk), "fields": p.data}, "in_stock": True})

        else:
            return Response(status=400)

    # print(model_to_dict(request.user))

    product_list_wishlist = product_list_wishlist
    data = {"user_folk": model_to_dict(request.user),
            "token": token,
            "cart_total": total_cart,
            "wishlist_total": total_wishlist,
            "cart_product": {"product_list": product_list_cart, "total": subtotal},
            "wishlist_product": {"products": product_list_wishlist},

            }
    return Response(data, status=200)


@api_view(["GET"])
def is_connected(request):
    if verify_user(request)["user"]:
        return Response(status=200)
    else:
        return Response(status=400)


@api_view(['GET', 'POST'])
def forgot_password(request):
    if request.method == 'POST':
        forgot_serializer = ForgotPasswordSerializer(data=request.data)
        if forgot_serializer.is_valid():

            user = Utilisateurs.objects.get(email=request.data['email'])
            current_site = get_current_site(request)
            message = render_to_string(
                "Applink/EmailForgot.html",
                {
                    "user": user,
                    "domain": current_site,
                    "token": PasswordResetTokenGenerator().make_token(user),
                    "uid": urlsafe_base64_encode(user.pk.bytes)
                }
            )

            email = forgot_serializer.validated_data.get('email')

            mail_subject = "Confirmation d'email"

            mail = EmailMessage(mail_subject, message, to=[email])

            mail.send()

            return Response(forgot_serializer.data, status=200)
        else:
            return Response(forgot_serializer.errors, status=400)


@api_view(['GET', 'POST'])
def forgot_password_change(request):
    if request.method == 'POST':
        forgot_password_serializer = ForgotSerializer(data=request.data)

        if forgot_password_serializer.is_valid():
            user = Utilisateurs.objects.get(email=request.session["user_email"])
            forgot_password_serializer.validated_data["Confpassword"] = make_password(
                forgot_password_serializer.validated_data.get("Confpassword"))
            user.__dict__update({'password': forgot_password_serializer.validated_data["Confpassword"]})
            user.save()

            return Response(forgot_password_serializer.data, status=200)

        else:
            return Response(forgot_password_serializer.errors, status=400)


@api_view(['GET'])
def get_all_user(request):
    users = Utilisateurs.objects.all()

    data_user = []

    for user in users:
        model_dict = model_to_dict(user)
        time_joined = user.date_joined
        time_login = user.last_login
        model_dict.update({'date_joined': time_joined.strftime("%Y-%m-%d %H:%M:%S"),
                           'last_login': time_login.strftime("%Y-%m-%d %H:%M:%S")
                           if time_login is not None else time_login,
                           }
                          )
        data_user.append({'user_pk': str(user.pk), 'user_data': model_dict})

    return Response({'users': data_user}, status=200)


@api_view(['GET'])
def delete_on_user(request):
    id = request.GET['id']
    id = str(id)
    id = id.replace('-', '')
    user = Utilisateurs.objects.get(pk=id)

    user.delete()

    return Response(status=200)


@api_view(['GET', 'POST'])
def contact_register(request):
    if request.method == 'POST':
        contact_serializer = ContactSerilalizer(data=request.data)
        if contact_serializer.is_valid():
            contact_serializer.save()

            return Response(status=200)
        else:
            return Response(contact_serializer.errors, status=400)


@api_view(['GET'])
def translate(request):
    if 'language' in request.GET and request.GET['language']:
        language = request.GET['language']
        if language in ['fr', 'en']:
            if language == 'fr':
                translation.activate(language)
                request.session['language'] = 'Français'
            if language == 'en':
                translation.activate(language)
                request.session['language'] = 'English'
    return Response(status=200)

# Create your views here.
