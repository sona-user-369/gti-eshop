import json

import flickrapi
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from elasticsearch_dsl.query import Q
import telegram

from Applink.serializer import UserRegisterSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login, logout, authenticate
from rest_framework.authentication import TokenAuthentication
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
import uuid

from DashBoard.Manage import FlickrAPICustom
from EShopGTI import settings
from EShopGTI.settings import MEDIA_URL
from ProdApp.document import DocumentProduit
from .Manage import *
import requests
from Applink.forms import *
from Applink.serializer import *
from .models import *


def home(request):
    request.session['cart'] = '{"produit_set": []}'
    request.session['wishlist'] = '{"produit_set" : []}'

    Register = RegisterForm()
    Login = LoginForm()
    categories = get_categorie(request)

    # Getting recents products
    recent_products = get_recent_products()

    # Getting best-selling products
    best_seller_products = get_best_seller(6)

    # Getting all
    all_categorie = Categorie.objects.all()

    context = {'Register': Register,
               'Login': Login,
               'username': upload_sense_data(request)['user'],
               'cart_count': upload_sense_data(request)['cart_count'],
               'wishlist_count': upload_sense_data(request)['wishlist_count'],
               'cart_product': upload_sense_data(request)['cart_product'],
               'total': upload_sense_data(request)['total'],
               'categories': categories,
               'recent': recent_products,
               'best_sellers': best_seller_products,
               'languages': upload_sense_data(request)['languages'],
               'copywrite_year': upload_sense_data(request)['copywrite_year'],
               }

    return render(request, 'home/index22.html', context)


def build_absolute_uri(request, url):
    site = get_current_site(request)
    return f"{site.scheme}://{site.domain}{reverse(url)}"


def share_message_telegram(request, image_url):
    bot = telegram.Bot(token='5874242082:AAH_aAKOHmzdIUNVfQ_qTqL88PnxtxPgmlw')

    chat_id = '5669217982'

    text = 'Hello check this out'
    path = str(request.path)
    url = path.replace('/telegram_send//', '')
    print(url)
    site = get_current_site(request)
    print(site)
    with open(url, 'rb') as image:
        bot.send_photo(chat_id=chat_id, photo=image, caption=text)

    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(uuid.UUID(bytes=urlsafe_base64_decode(uidb64)))

        user = Utilisateurs.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Utilisateurs.DoesNotExist):
        user = None
    if user is not None and PasswordResetTokenGenerator().check_token(user=user, token=token):
        user.is_active = True
        user.save()

        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid')


def activate_forgout(request, uidb64, token):
    try:
        uid = force_str(uuid.UUID(bytes=urlsafe_base64_decode(uidb64)))

        user = Utilisateurs.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Utilisateurs.DoesNotExist):
        user = None
    if user is not None and PasswordResetTokenGenerator().check_token(user=user, token=token):
        request.session["link_is_clicked"] = 1
        request.session["user_email"] = user.email

        return redirect('forgot_render')
    else:
        return HttpResponse('Activation link is invalid')


def forgout_pass(request):
    forgot_form = ForgotForm()
    try:
        session = request.session["link_is_clicked"]
    except:
        return redirect('home')

    if not session:
        return redirect('home')
    else:
        request.session["link_is_clicked"] = 0

    return render(request, 'home/forgotPassword.html',
                  {'ForgotForm': forgot_form,
                   'languages': upload_sense_data(request)['languages'],
                   'copywrite_year': upload_sense_data(request)['copywrite_year']
                   })


#####Logout User
def logout_user(request):
    if not verify_user(request)["user"]:
        return redirect('home')

    if supp_logout(request):
        return redirect('home')


def delete_user(request):
    if supp_delete(request):
        return redirect('home')


def product(request, id):
    id_produit = str(id)
    id_produit = id_produit.replace('-', '')
    produit = Produit.objects.get(pk=id_produit)
    same_product = Produit.objects.filter(categorie=produit.categorie)
    i = 0
    same_product_copy = list(same_product)
    same_product_copy.pop(same_product_copy.index(produit))
    four_same_product = []
    if len(same_product_copy) < 4:
        len_result = len(same_product_copy)
    else:
        len_result = 4

    for i in range(len_result):
        len_review = len(Avis.objects.filter(produit=same_product_copy[i]))
        note_for_product = 0
        for avis in Avis.objects.filter(produit=same_product_copy[i]):
            note_for_product += avis.rating
        try:
            note_for_product = int(note_for_product / len_review)
        except:
            pass
        four_same_product.append(
            {'produit': same_product_copy[i], 'review': len_review, 'note_product': note_for_product})

    avis_more = []
    avis = Avis.objects.filter(produit=produit)

    date = ""
    note = 0
    for a in avis:
        date_all = timezone.now() - a.date
        if date_all.days:
            if date_all.days < 7:
                date = str(date_all.days) + " jours"
            else:
                if date_all.days >= 7 and date_all.days < 30:
                    date = str(int(date_all.days / 7)) + " semaines"
                else:
                    if date_all.days >= 30 and date_all.days < 30 * 12:
                        date = str(int(date_all.days / 30)) + "mois"
                    else:
                        date = str(int(date_all.days / (30 * 12))) + "ans"


        else:
            if date_all.seconds:
                if date_all.seconds < 60:
                    date = str(date_all.seconds) + " secondes"
                else:
                    if date_all.seconds >= 60 and date_all.seconds < 3600:
                        date = str(int(date_all.seconds / 60)) + " minutes"
                    else:
                        date = str(int(date_all.seconds / 3600)) + " heures"

        note += a.rating
        avis_more.append({'avis': a, 'ago': date})
    try:
        note = int(note / len(avis_more))
    except:
        pass
    Register = RegisterForm()
    Login = LoginForm()
    Review = ReviewForm()

    context = {'Register': Register,
               'Login': Login,
               'Review': Review,
               'username': upload_sense_data(request)['user'],
               'cart_count': upload_sense_data(request)['cart_count'],
               'wishlist_count': upload_sense_data(request)['wishlist_count'],
               'cart_product': upload_sense_data(request)['cart_product'],
               'total': upload_sense_data(request)['total'],
               'produit': produit,
               'four_product': four_same_product,
               'avis': avis_more,
               'avis_count': len(avis_more),
               'note': note,
               'languages': upload_sense_data(request)['languages'],
               'copywrite_year': upload_sense_data(request)['copywrite_year'],
               }

    return render(request, 'home/product.html', context)


def cart(request):
    Register = RegisterForm()
    Login = LoginForm()

    # user = verify_user(request)["user"]


    context = {'Register': Register,
               'Login': Login,
               'username': upload_sense_data(request)['user'],
               'cart_count': upload_sense_data(request)['cart_count'],
               'wishlist_count': upload_sense_data(request)['wishlist_count'],
               'cart_product': upload_sense_data(request)['cart_product'],
               'total': upload_sense_data(request)['total'],
               'languages': upload_sense_data(request)['languages'],
               'copywrite_year': upload_sense_data(request)['copywrite_year'],
               }

    # if not user:
    #     return redirect('home')

    return render(request, 'home/cart.html', context)


def test(request):
    return render(request, 'home/Test.html')


def wishlist(request):
    Register = RegisterForm()
    Login = LoginForm()

    all_categorie = Categorie.objects.all()

    context = {'Register': Register,
               'Login': Login,
               'username': upload_sense_data(request)['user'],
               'cart_count': upload_sense_data(request)['cart_count'],
               'wishlist_count': upload_sense_data(request)['wishlist_count'],
               'cart_product': upload_sense_data(request)['cart_product'],
               'wishlist_product': upload_sense_data(request)['wishlist_product'],
               'total': upload_sense_data(request)['total'],
               'languages': upload_sense_data(request)['languages'],
               'copywrite_year': upload_sense_data(request)['copywrite_year'],
               }
    # if not user:
    #     return redirect('home')

    return render(request, 'home/wishlist.html', context)


def category(request):

    product = Produit.objects.filter(is_archive=False)
    categorie = Categorie.objects.all()
    categorie_products = []
    product_info = []
    query_not_match = 0
    set_cookie(request)
    try:
        session = request.session['search_phrase']
    except:
        session = None

    try:
        session_categorie = request.session['category_name']
    except:
        session_categorie = None

    if session is not None:
        search_done = search_for_product(session)
        request.session['search_phrase'] = None
        if search_done['data'] is not None:
            product_info = search_done['data']
        else:

            query_not_match = 1

    else:
        if session_categorie is not None:
            request.session['category_name'] = None
            category_name = session_categorie
            got_categorie = Categorie.objects.get(nom=category_name)
            products = Produit.objects.filter(categorie=got_categorie, is_archive=False)
            for p in products:
                note_for_product = 0
                len_review = len(Avis.objects.filter(produit=p))
                for avis in Avis.objects.filter(produit=p):
                    note_for_product += avis.rating
                try:
                    note_for_product = int(note_for_product / len_review)
                except:
                    pass
                product_info.append({'produit': p, 'review': len_review, 'note_product': note_for_product})
        else:
            for p in product:
                note_for_product = 0
                len_review = len(Avis.objects.filter(produit=p))
                for avis in Avis.objects.filter(produit=p):
                    note_for_product += avis.rating
                try:
                    note_for_product = int(note_for_product / len_review)
                except:
                    pass
                product_info.append({'produit': p, 'review': len_review, 'note_product': note_for_product})

    paginator = Paginator(product_info, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for c in categorie:
        try:
            p = Produit.objects.filter(categorie=c, is_archive=False)
            categorie_products.append({'categorie': c, 'length': len(p)})
        except:
            pass
    Register = RegisterForm()
    Login = LoginForm()



    context = {'Register': Register,
               'Login': Login,
               'username': upload_sense_data(request)['user'],
               'cart_count': upload_sense_data(request)['cart_count'],
               'wishlist_count': upload_sense_data(request)['wishlist_count'],
               'cart_product': upload_sense_data(request)['cart_product'],
               'wishlist_product': upload_sense_data(request)['wishlist_product'],
               'product': product_info,
               'total': upload_sense_data(request)['total'],
               'categorie': categorie_products,
               'page_obj': page_obj,
               'query_not_match': query_not_match,
               'languages': upload_sense_data(request)['languages'],
               'total_products': len(product),
               'copywrite_year': upload_sense_data(request)['copywrite_year']
               }

    return render(request, 'home/category.html', context)


def retrieve_categorie(request, id):
    id = str(id)
    id = id.replace('-', '')

    categorie = Categorie.objects.get(pk=id)

    request.session['category_name'] = categorie.nom

    return redirect('category')


def search_product(request):
    categorie = Categorie.objects.all()
    categorie_products = []
    product_info = []

    q = Q(
        'multi_match',
        query=request.POST['search'],

        fields=[
            'nom'
        ])

    search = DocumentProduit.search().query(q)
    response = search.execute()
    search = search.to_queryset()

    for p in search:
        note_for_product = 0
        len_review = len(Avis.objects.filter(produit=p))
        for avis in Avis.objects.filter(produit=p):
            note_for_product += avis.rating
        try:
            note_for_product = int(note_for_product / len_review)
        except:
            pass
        product_info.append({'produit': p, 'review': len_review, 'note_product': note_for_product})

    paginator = Paginator(search, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for c in categorie:
        try:
            p = Produit.objects.filter(categorie=c)
            categorie_products.append({'categorie': c, 'length': len(p)})
        except:
            pass
    Register = RegisterForm()
    Login = LoginForm()



    context = {'Register': Register,
               'Login': Login,
               'username': upload_sense_data(request)['user'],
               'cart_count': upload_sense_data['cart_count'],
               'wishlist_count': upload_sense_data(request)['wishlist_count'],
               'cart_product': upload_sense_data(request)['cart_product'],
               'wishlist_product': upload_sense_data(request)['wishlist_product'],
               'product': product_info,
               'total': upload_sense_data(request)['total'],
               'categorie': categorie_products,
               'page_obj': page_obj,
               'languages': upload_sense_data(request)['languages'],
               'copywrite_year': upload_sense_data(request)['copywrite_year']
               }

    return render(request, 'home/category.html', context)


def about(request):
    Register = RegisterForm()
    Login = LoginForm()
    copywrite_year = get_copywrite_year()
    user = verify_user(request)["user"]
    cart_count = verify_user(request)["cart_total"]
    wishlist_count = verify_user(request)["wishlist_total"]
    wishlist_product = verify_user(request)["wishlist_product"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    languages = select_languages(request)

    context = {'Register': Register,
               'Login': Login,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'wishlist_product': wishlist_product,
               'total': total,
               'languages': languages,
               'copywrite_year': copywrite_year
               }

    return render(request, 'home/about2.html', context)


def contact(request):
    Register = RegisterForm()
    Login = LoginForm()
    ContactEnter = ContactForm()
    user = verify_user(request)["user"]
    cart_count = verify_user(request)["cart_total"]
    wishlist_count = verify_user(request)["wishlist_total"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    languages = select_languages(request)
    copywrite_year = get_copywrite_year()
    context = {'Register': Register,
               'Login': Login,
               'ContactEnter': ContactEnter,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'total': total,
               'languages': languages,
               'copywrite_year': copywrite_year
               }

    return render(request, 'home/contact.html', context)


def thankregistration(request, user):
    return render(request, 'home/ThankRegistration.html', {'user': str(user)})


def LinkValidation(request):
    return render(request, 'home/ValidLink.html')


def profil(request):
    user = verify_user(request)["user"]
    if not user:
        return redirect('home')
    UpForm = UpdateForm(user)

    Register = RegisterForm()
    Login = LoginForm()

    cart_count = verify_user(request)["cart_total"]
    wishlist_count = verify_user(request)["wishlist_total"]
    wishlist_product = verify_user(request)["wishlist_product"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    languages = select_languages(request)
    copywrite_year = get_copywrite_year()

    context = {'Register': Register,
               'Login': Login,
               'UpForm': UpForm,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'wishlist_product': wishlist_product,
               'total': total,
               'languages': languages,
               'copywrite_year': copywrite_year,
               }

    return render(request, 'home/OtherProfil.html', context)


def update_user(request):
    if verify_update(request):
        return redirect('my_profil')
    else:
        return redirect('my_profil')


def google_login(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('google_login')
    )
    if ('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        if email:
            try:
                user = Utilisateurs.objects.get(email=email)
            except Utilisateurs.DoesNotExist:
                user = None
            data = {
                'first_name': user_data.get('name', '').split()[0],
                'last_name': user_data.get('family_name'),

                'is_active': True
            }
            if user is not None:

                user.__dict__.update(data)
                user.save()
                user.backend = settings.AUTHENTICATION_BACKENDS[0]
                print("trtrtrrtttttttttttttttttttttttttttttttttttttttttt")

                url_login = "http://127.0.0.1:8000/link/login"
                # print(model_to_dict(user))
                response = requests.post(url_login,
                                         data={'email': user.email, 'password': user.password, 'from_google': 1,
                                               'verify_superuser': 0})
                request.session['token'] = response.json()['token']
                primary_key = str(user.pk)
                primary_key = primary_key.replace('-', '')
                request.session["user_primary"] = primary_key
                print(response.json())
                return redirect('/')
            else:
                data['is_active'] = False
                data['email'] = email
                user = Utilisateurs.objects.create(email=email)
                user.__dict__.update(data)
                user.save()
                User = GoogleSerializer(data=data)
                if User.is_valid():

                    request.session["google"] = User.data

                    print(User.data)
                else:
                    print(User.errors)

                return redirect('fill')


        else:
            messages.error(
                request,
                'Unable to login with Gmail Please try again'
            )

            return redirect('/')
    else:
        print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)


def fill(request):
    FillForm = RegisterForm(request.session["google"])
    Register = RegisterForm()
    Login = LoginForm()
    copywrite_year = get_copywrite_year()

    user = verify_user(request)["user"]
    cart_count = verify_user(request)["cart_total"]
    wishlist_count = verify_user(request)["wishlist_total"]
    wishlist_product = verify_user(request)["wishlist_product"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    languages = select_languages(request)

    context = {'Register': Register,
               'Login': Login,
               'FillForm': FillForm,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'wishlist_product': wishlist_product,
               'total': total,
               'languages': languages,
               'copywrite_year': copywrite_year,
               }

    return render(request, 'home/Fillup.html', context)


def password_change(request):
    copywrite_year = get_copywrite_year()
    user = verify_user(request)["user"]
    if not user:
        return redirect('home')
    PasswordForm = ChangeForm()
    Register = RegisterForm()
    Login = LoginForm()

    cart_count = verify_user(request)["cart_total"]
    wishlist_count = verify_user(request)["wishlist_total"]
    wishlist_product = verify_user(request)["wishlist_product"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    languages = select_languages(request)

    context = {'Register': Register,
               'Login': Login,
               'PasswordForm': PasswordForm,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'wishlist_product': wishlist_product,
               'total': total,
               'languages': languages,
               'copywrite_year': copywrite_year
               }

    return render(request, 'home/PasswordChange.html', context)


def invoice_order(request):
    user = verify_user(request)["user"]
    if not user:
        return redirect('home')

    cart_count = verify_user(request)["cart_total"]
    wishlist_count = verify_user(request)["wishlist_total"]
    wishlist_product = verify_user(request)["wishlist_product"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    invoice = get_invoice_or_none(request)
    Register = RegisterForm()
    Login = LoginForm()
    languages = select_languages(request)
    copywrite_year = get_copywrite_year()

    context = {'Register': Register,
               'Login': Login,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'wishlist_product': wishlist_product,
               'total': total,
               'invoice': invoice,
               'languages': languages,
               'copywrite_year': copywrite_year,
               }
    print(invoice)
    print('ccccccccccccc')
    return render(request, 'home/invoice.html', context)


def shipping(request):
    user = verify_user(request)["user"]
    if not user:
        return redirect('home')

    cart_count = verify_user(request)["cart_total"]
    if cart_count == 0:
        return redirect('home')
    wishlist_count = verify_user(request)["wishlist_total"]
    wishlist_product = verify_user(request)["wishlist_product"]
    cart_product = verify_user(request)["cart_product"]
    total = verify_user(request)["total"]
    ship_form = ShipForm()
    languages = select_languages(request)
    copywrite_year = get_copywrite_year()

    context = {'ShipForm': ship_form,
               'username': user,
               'cart_count': cart_count,
               'wishlist_count': wishlist_count,
               'cart_product': cart_product,
               'wishlist_product': wishlist_product,
               'product': product,
               'total': total,
               'languages': languages,
               'copywrite_year': copywrite_year
               }

    return render(request, 'home/shipping.html', context)

def flickr_callback(request):
    if request.session.get('token_flickr') is not None:
        f = FlickrAPICustom(
            settings.FLICKR_API_KEY,
            settings.FLICKR_SECRET_KEY,
            store_token=False)
        frob = None
        token = None
        try:
            print(request.GET)
            request.session['token_flickr'] = token
        except Exception:
            pass
    return redirect('dash')
# Create your views here.
