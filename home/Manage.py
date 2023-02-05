'''Write by Davakan Donatien'''
import datetime
from json import JSONDecoder
import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.forms import model_to_dict
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from elasticsearch_dsl.query import Q
from Applink.forms import LoginForm, RegisterForm
from django.contrib.sites.shortcuts import get_current_site

import json

from EShopGTI import settings
from EShopGTI.settings import SITE_HOSTNAME
from ProdApp.document import DocumentProduit
from home.models import Panier, Favoris, Avis, Produit, Commandes, CommandeProduit


def verify_user(object):
    url = "http://" + SITE_HOSTNAME + "/link/sample"

    # print(object.session['token'])
    if "token" in object.session:
        print('Token')
        response = requests.get(url, headers={'Authorization': 'Token ' + object.session["token"]})
        response.encoding = 'utf-8'

    else:
        print('Not Token')
        response = requests.get(url)
        response.encoding = 'utf-8'
    if response.status_code != 200:

        data = {'user': None,
                'token': None,
                'cart_total': None,
                'wishlist_total': None,
                'cart_product': None,
                'wishlist_product': None,
                'total': None,

                }
    else:
        # requests.request.session["user_primary"] = object.session["user_primary"]

        user = response.json()["user_folk"]
        token = response.json()["token"]

        data = {'user': user,
                'token': token,
                'cart_total': response.json()["cart_total"],
                'total': response.json()["cart_product"]["total"],
                'wishlist_total': response.json()["wishlist_total"],
                'cart_product': response.json()["cart_product"],
                'wishlist_product': response.json()["wishlist_product"],

                }
    return data


def get_invoice_or_none(object):
    if 'user_primary' in object.session:
        url_product = "http://" + SITE_HOSTNAME + '/extlink/commande/' + object.session["user_primary"]

        if verify_user(object)['user']:
            print('ooooooooo')
            response = requests.get(url_product)
            if response.status_code == 200:
                data = response.json()
            else:
                data = None
            return data
        else:
            print('nnnnnnnnnnnnn')
            return None
    else:
        return None


def supp_logout(object):
    url = "http://" + SITE_HOSTNAME + "/link/logout"
    if "token" in object.session:
        response = requests.delete(url, headers={'Authorization': 'Token ' + object.session["token"]})
    else:
        response = requests.delete(url)

    if response.status_code != 200:
        return False
    else:
        if response.status_code == 200:
            return True
        else:
            return False


def supp_delete(object):
    url = "http://" + SITE_HOSTNAME + "/link/delete/" + object.session["user_primary"]
    if "token" in object.session:
        response = requests.delete(url, headers={'Authorization': 'Token ' + object.session["token"]})
    else:
        response = requests.delete(url)

    if response.status_code != 200:
        return False
    else:
        if response.status_code == 200:
            return True
        else:
            return False


def verify_update(object):
    url = "http://" + SITE_HOSTNAME + "/link/update/" + object.session["user_primary"]
    if "token" in object.session:
        print(object.POST)
        response = requests.put(url, data=object.POST, headers={'Authorization': 'Token ' + object.session["token"]})
    else:
        response = requests.put(url, data=object.POST)
    print(response.json())
    if response.status_code == 401:
        print("erreur")
        return False
    else:
        if response.status_code == 200:
            return True
        else:
            return False


def subscribe(object):
    api_key = settings.MAILCHIMP_API_KEY
    server = settings.MAILCHIMP_DATA_CENTER
    list_id = settings.MAILCHIMP_EMAIL_LIST_ID
    mailchimp = Client()
    mailchimp.set_config(
        {
            "api_key": api_key,
            "server": server,
        }
    )

    member_info = {
        "email_address": object,
        "status": "subscribed",
    }

    try:

        response = mailchimp.lists.add_list_member(list_id, member_info)
        print(response)
        return True
    except ApiClientError as error:
        print(error.text)
        return False


def search_for_product(object):
    product_info = []

    q = Q(
        'multi_match',
        query=object,

        fields=[
            'nom'
        ])

    search = DocumentProduit.search().query(q)
    response = search.execute()
    the_list = []
    search = search.to_queryset()
    if len(search) != 0:

        for p in search:
            if p.is_archive == False:
                len_review = len(Avis.objects.filter(produit=p))
                product_info.append({'produit': p, 'review': len_review})
                the_list.append(p)

        if the_list == []:
            return {'result': True, 'data': None}
        return {'result': True, 'data': product_info}
    else:
        return {'result': True, 'data': None}


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            if isinstance(o, Panier):
                return model_to_dict(o)
            else:
                if isinstance(o, Favoris):
                    return model_to_dict(o)
            return super().default(o)


def get_categorie(object):
    url = 'http://' + SITE_HOSTNAME + '/extlink/all_tables_categories'

    response = requests.get(url)
    resp_json = response.json()
    return resp_json['categories']


class ExtendedDecoder(JSONDecoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            if isinstance(o, Panier):
                return model_to_dict(o)
            else:
                if isinstance(o, Favoris):
                    return model_to_dict(o)
            return super().default(o)


def get_product_quantity(_dict):
    """use for key sort a list of dict. It returns the quantity of product"""
    return _dict['quantite']


def get_product_list(_list):
    """use for getting only products"""

    _list_product = []
    for _instance in _list:
        _list_product.append(_instance['produit'])
    return _list_product


def get_recent_products():
    """Get recent products """
    products_recent = Produit.objects.filter(is_archive=False).order_by('-date_de_stock')
    products_recent_six = []
    for i in range(6):
        try:
            note_for_product = 0
            len_review = len(Avis.objects.filter(produit=products_recent[i]))
            for avis in Avis.objects.filter(produit=products_recent[i]):
                note_for_product += avis.rating
            try:
                note_for_product = int(note_for_product / len_review)
            except:
                pass
            products_recent_six.append(
                {'produit': products_recent[i], 'review': len_review, 'note_product': note_for_product})
        except:
            pass
    return products_recent_six


def get_best_seller(dim):
    """Get the best sellers products"""

    product_best_sell = []
    final_products = []
    all_commandes = Commandes.objects.all()
    for commande in all_commandes:
        for product in commande.produit_set.all():
            quantity_product = CommandeProduit(commande=commande, produit=product).quantite
            product_best_sell.append({'produit': product, 'quantite': quantity_product})

    sorted_products = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    for i in range(dim):
        try:
            if len(final_products) != 0:
                if sorted_products[i]['produit'] in get_product_list(final_products):
                    pass
                else:
                    note_for_product = 0
                    len_review = len(Avis.objects.filter(produit=sorted_products[i]['produit']))
                    for avis in Avis.objects.filter(produit=sorted_products[i]['produit']):
                        note_for_product += avis.rating
                    try:
                        note_for_product = int(note_for_product / len_review)
                    except:
                        pass
                    final_products.append({'produit': sorted_products[i]['produit'], 'review': len_review,
                                           'note_product': note_for_product})
            else:
                note_for_product = 0
                len_review = len(Avis.objects.filter(produit=sorted_products[i]['produit']))
                for avis in Avis.objects.filter(produit=sorted_products[i]['produit']):
                    note_for_product += avis.rating
                try:
                    note_for_product = int(note_for_product / len_review)
                except:
                    pass
                final_products.append(
                    {'produit': sorted_products[i]['produit'], 'review': len_review, 'note_product': note_for_product})
        except:
            pass
    return final_products


def select_languages(object):
    if 'language' in object.session:
        if object.session['language'] == 'Français':
            second_language = 'English'
            all_language = {'selected': object.session['language'], 'second': second_language}
        else:
            second_language = 'Français'
            all_language = {'selected': object.session['language'], 'second': second_language}
    else:
        all_language = {'selected': 'Français', 'second': 'English'}

    return all_language


def get_copywrite_year():
    date = datetime.datetime.utcnow()
    year = date.year
    return year


def set_cookie(object):
    if 'cart' not in object.COOKIES:
        object.COOKIES['cart'] = ''


def upload_sense_data(object):
    # user = verify_user(request)["user"]
    cart = object.session.get('cart')
    cart = json.loads(cart) if cart is not None else None
    wishlist = object.session.get('wishlist')
    wishlist = json.loads(wishlist) if wishlist is not None else None
    user = verify_user(object)["user"]
    cart_count = len(cart['produit_set']) if cart is not None else 0
    # cart_count = verify_user(request)["cart_total"]
    wishlist_count = len(wishlist['produit_set']) if wishlist is not None else 0
    wishlist_product = wishlist['produit_set'] if wishlist is not None else []
    cart_product = cart['produit_set'] if cart is not None else []
    print(cart_product)
    # cart_product = verify_user(request)["cart_product"]
    total = 0
    if cart is not None:
        for p in cart['produit_set']:
            total += p['quantite'] * p['prix']
    # total = verify_user(request)["total"]
    languages = select_languages(object)
    copywrite_year = get_copywrite_year()

    data = {
        'user': user,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'cart_product': cart_product,
        'wishlist_product': wishlist_product,
        'total': total,
        'languages': languages,
        'copywrite_year': copywrite_year

    }
    return data
