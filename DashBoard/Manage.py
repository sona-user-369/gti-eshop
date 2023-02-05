import requests
import six
from dateutil.relativedelta import relativedelta
from django.contrib.sites.shortcuts import get_current_site
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from Applink.serializer import UserSerializer
from EShopGTI.settings import SITE_HOSTNAME
from ProdApp.serializer import ProduitSerializer
from home.Manage import verify_user, get_product_quantity
from home.models import Commandes, CommandeProduit, Utilisateurs
from flickrapi.core import FlickrAPI, authenticator


def get_tables(object):
    url_1 = 'http://' + SITE_HOSTNAME + '/link/all_tables_users'
    url_2 = 'http://' + SITE_HOSTNAME + '/extlink/all_tables_products'
    url_3 = 'http://' + SITE_HOSTNAME + '/extlink/all_tables_categories'
    url_4 = 'http://' + SITE_HOSTNAME + '/extlink/all_tables_sousCategories'
    url_5 = 'http://' + SITE_HOSTNAME + '/extlink/all_tables_reviews'
    url_6 = 'http://' + SITE_HOSTNAME + '/extlink/all_tables_commandes'

    response_users = requests.get(url_1)
    response_products = requests.get(url_2)
    response_categories = requests.get(url_3)
    response_sousCategorie = requests.get(url_4)
    response_reviews = requests.get(url_5)
    response_commandes = requests.get(url_6)
    print(response_sousCategorie.status_code)
    data = {
        'data_users': response_users.json()['users'],
        'data_products': response_products.json()['products'],
        'data_categories': response_categories.json()['categories'],
        'data_sousCategories': response_sousCategorie.json()['sousCategories'],
        'data_reviews': response_reviews.json()['reviews'],
        'data_commandes': response_commandes.json()['commandes']
    }

    return data


def decorator_dashboard(func):
    def handle(object):
        user = verify_user(object)['user']
        if user is None:
            return redirect('login_admin')

        return func(object)

    return handle


def decorator_dashboard_ext(func):
    def handle(object, **kwarg):
        user = verify_user(object)['user']
        if user is None:
            return redirect('login_admin')

        return func(object, **kwarg)

    return handle


def combine_products(_list):
    """combine products with same name by quantity sold"""

    _final_list = []
    _list_copy = _list.copy()
    for _instance in _list_copy:
        quantity_for_products = int(_instance['quantite'])
        _list_copy.pop(_list_copy.index(_instance))
        for _instance_ext in _list_copy:
            if _instance_ext['produit'] == _instance['produit']:
                quantity_for_products += int(_instance_ext['quantite'])
        _final_list.append({
            'produit_pk': _instance['produit_pk'],
            'produit': _instance['produit'],
            'quantite': quantity_for_products,
            'sales_time': _instance['sales_time']
        })

    return _final_list


def get_best_sellers_time():
    """Get the best sellers based on time (day, month, year)"""

    all_commandes = Commandes.objects.all()

    # for day

    product_best_sell = []

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 1:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande, })
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_day = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    # for month

    product_best_sell = []

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 31:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass

    product_best_sell = combine_products(product_best_sell)

    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})
    sorted_products_month = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    # for year

    product_best_sell = []

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 366:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})
    sorted_products_year = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    final_products = [sorted_products_day, sorted_products_month, sorted_products_year]

    return final_products


def get_recent_sales():
    """Get recent sales base on time"""

    recent_sales_day = []
    recent_sales_month = []
    recent_sales_year = []

    # for day
    all_commandes = Commandes.objects.all()

    for commande in all_commandes:
        products_day = []
        products_month = []
        products_year = []

        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 1:
            print(len(commande.produit_set.all()))
            for product in commande.produit_set.all():
                quantite = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                products_day.append({'product': product,
                                     'quantite': quantite})

            products_day_copy = products_day.copy()
            products_day_copy.pop(0)
            recent_sales_day.append({'user': commande.utilisateur.first_name + " " + commande.utilisateur.last_name,
                                     'commande': commande,
                                     'product_commande': products_day,
                                     'first_product': products_day[0],
                                     'product_commande_ext': products_day_copy,
                                     'len_products': len(products_day)})
        else:
            if this_date.days <= 31:
                for product in commande.produit_set.all():
                    quantite = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    products_month.append({'product': product,
                                           'product_pk': product.pk,
                                           'quantite': quantite})
                products_month_copy = products_month.copy()
                products_month_copy.pop(0)
                recent_sales_month.append(
                    {'user': commande.utilisateur.first_name + " " + commande.utilisateur.last_name,
                     'commande': commande,
                     'product_commande': products_month,
                     'first_product': products_month[0],
                     'product_commande_ext': products_month_copy,
                     'len_products': len(products_month)})

            else:
                for product in commande.produit_set.all():
                    quantite = CommandeProduit.objects.get(commande=commande, produit=product)
                    products_year.append({'product': model_to_dict(product),
                                          'product_pk': product.pk,
                                          'quantite': quantite})
                recent_sales_year.append(
                    {'user': commande.utilisateur.first_name + " " + commande.utilisateur.last_name,
                     'commande_pk': commande.pk,
                     'product_commande': products_day})
    final_sales = [recent_sales_day, recent_sales_month, recent_sales_year]

    return final_sales


def stats_sales():
    all_commandes = Commandes.objects.all()
    # this day
    product_best_sell = []
    best_sales_day = get_best_sellers_time()[0]
    sold = 0
    for _instance in best_sales_day:
        sold += _instance['quantite']

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 2:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_2day = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    sorted_copy = sorted_products_2day.copy()
    for _instance in best_sales_day:
        sorted_copy.pop(sorted_copy.index(_instance))

    sold_2days = 0
    for _instance in sorted_copy:
        sold_2days += _instance['quantite']

    stats_day = sold - sold_2days
    if stats_day < 100:
        percent = stats_day
    else:
        percent = 99

    stats_day_total = [sold, percent]

    # for month

    product_best_sell = []
    best_sales_month = get_best_sellers_time()[1]
    sold = 0
    for _instance in best_sales_month:
        sold += _instance['quantite']

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 62:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_2month = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    sorted_copy = sorted_products_2month.copy()
    print(sorted_copy)
    print(best_sales_month)
    for _instance in best_sales_month:
        sorted_copy.pop(sorted_copy.index(_instance))

    sold_2month = 0
    for _instance in sorted_copy:
        sold_2month += _instance['quantite']

    stats_month = sold - sold_2month
    if stats_month < 100:
        percent = stats_month
    else:
        percent = 99

    stats_month_total = [sold, percent]

    # for year

    product_best_sell = []
    best_sales_year = get_best_sellers_time()[2]
    sold = 0
    for _instance in best_sales_year:
        sold += _instance['quantite']

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 732:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_2year = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    sorted_copy = sorted_products_2year.copy()
    for _instance in best_sales_year:
        sorted_copy.pop(sorted_copy.index(_instance))

    sold_2year = 0
    for _instance in sorted_copy:
        sold_2year += _instance['quantite']

    stats_year = sold - sold_2year
    if stats_year < 100:
        percent = stats_year
    else:
        percent = 99

    stats_year_total = [sold, percent]

    final_stats = [stats_day_total, stats_month_total, stats_year_total]

    return final_stats


def stats_revenu():
    all_commandes = Commandes.objects.all()
    # this day
    product_best_sell = []
    best_sales_day = get_best_sellers_time()[0]
    sold = 0
    for _instance in best_sales_day:
        sold += _instance['revenue']

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 2:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_2day = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    sorted_copy = sorted_products_2day.copy()
    for _instance in best_sales_day:
        sorted_copy.pop(sorted_copy.index(_instance))

    sold_2days = 0
    for _instance in sorted_copy:
        sold_2days += _instance['revenue']

    stats_day = sold - sold_2days
    if stats_day < 100:
        percent = stats_day
    else:
        percent = 99

    stats_day_total = [sold, percent]

    # for month

    product_best_sell = []
    best_sales_month = get_best_sellers_time()[1]
    sold = 0
    for _instance in best_sales_month:
        sold += _instance['revenue']

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 62:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_2month = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    sorted_copy = sorted_products_2month.copy()
    for _instance in best_sales_month:
        sorted_copy.pop(sorted_copy.index(_instance))

    sold_2month = 0
    for _instance in sorted_copy:
        sold_2month += _instance['revenue']

    stats_month = sold - sold_2month
    if stats_month < 100:
        percent = stats_month
    else:
        percent = 99

    stats_month_total = [sold, percent]

    # for year

    product_best_sell = []
    best_sales_year = get_best_sellers_time()[2]
    sold = 0
    for _instance in best_sales_year:
        sold += _instance['revenue']

    for commande in all_commandes:
        this_date = timezone.now() - commande.date_commande
        if this_date.days <= 732:
            for product in commande.produit_set.all():
                product_serializer = ProduitSerializer(data=model_to_dict(product))
                if product_serializer.is_valid():
                    quantity_product = CommandeProduit.objects.get(commande=commande, produit=product).quantite
                    product_best_sell.append({
                        'produit_pk': product.pk,
                        'produit': product_serializer.data,
                        'quantite': quantity_product,
                        'sales_time': commande.date_commande})
        else:
            pass
    product_best_sell = combine_products(product_best_sell)
    for _instance in product_best_sell:
        _instance.update({'revenue': _instance['produit']['prix'] * _instance['quantite']})

    sorted_products_2year = sorted(product_best_sell, key=get_product_quantity, reverse=True)

    sorted_copy = sorted_products_2year.copy()
    for _instance in best_sales_year:
        sorted_copy.pop(sorted_copy.index(_instance))

    sold_2year = 0
    for _instance in sorted_copy:
        sold_2year += _instance['revenue']

    stats_year = sold - sold_2year
    if stats_year < 100:
        percent = stats_year
    else:
        percent = 99

    stats_year_total = [sold, percent]

    final_stats = [stats_day_total, stats_month_total, stats_year_total]

    return final_stats


def stats_customer():
    all_users = Utilisateurs.objects.filter(is_active=True)
    user_days = 0
    user_month = 0
    user_year = 0

    user_2days = 0
    user_2month = 0
    user_2year = 0

    # for day

    for user in all_users:
        date_user = timezone.now() - user.date_joined
        if date_user.days <= 1:
            user_days += 1

        if date_user.days <= 31:
            user_month += 1

        if date_user.days <= 366:
            user_year += 1

    for user in all_users:
        date_user = timezone.now() - user.date_joined
        if date_user.days <= 2:
            user_2days += 1

        if date_user.days <= 62:
            user_2month += 1

        if date_user.days <= 732:
            user_2year += 1

    # for days

    stats_user_2days = user_2days - user_days
    stats_user_days = user_days - stats_user_2days
    if stats_user_days < 100:
        percent = stats_user_days
    else:
        percent = 99
    final_days = [user_days, percent]

    stats_user_2month = user_2month - user_month
    stats_user_month = user_month - stats_user_2month
    if stats_user_month < 100:
        percent = stats_user_month
    else:
        percent = 99
    final_month = [user_month, percent]

    stats_user_2year = user_2year - user_year
    stats_user_year = user_year - stats_user_2year
    if stats_user_year < 100:
        percent = stats_user_year
    else:
        percent = 99
    final_year = [user_year, percent]

    final_users = [final_days, final_month, final_year]

    return final_users


def customer_data():
    all_users = Utilisateurs.objects.filter(is_active=True)

    data_day = []
    data_month = []
    data_year = []
    for user in all_users:
        delta = timezone.now() - user.date_joined
        if delta.days <= 1:
            data_day.append(user.date_joined)
        if delta.days <= 31:
            data_month.append(user.date_joined)
        if delta.days <= 366:
            data_year.append(user.date_joined)

    final_customer = [data_day, data_month, data_year]
    return final_customer


def stats_chart():
    best_sales_day = get_best_sellers_time()[0]
    best_sales_month = get_best_sellers_time()[1]
    best_sales_year = get_best_sellers_time()[2]

    customer_day = customer_data()[0]
    customer_month = customer_data()[1]
    customer_year = customer_data()[2]

    day_intervals = []
    month_intervals = []
    year_intervals = []
    init_time = timezone.now()
    for i in range(6):
        day_intervals.append(init_time - relativedelta(hours=4 * i))
        month_intervals.append(init_time - relativedelta(days=5 * i))
        year_intervals.append(init_time - relativedelta(months=2 * i))

    total_day = []
    for i in range(6):
        count_for_day_qty = 0
        count_for_day_rev = 0
        count_for_day_cust = 0
        _list_day = []
        for sales in best_sales_day:
            if sales['sales_time'] < day_intervals[i]:
                count_for_day_qty += sales['quantite']
                count_for_day_rev += sales['revenue']

        for user_time in customer_day:
            if user_time < day_intervals[i]:
                count_for_day_cust += 1

        total_day.append([count_for_day_qty, count_for_day_rev, count_for_day_cust])

    total_month = []
    for i in range(6):
        count_for_month_qty = 0
        count_for_month_rev = 0
        count_for_month_cust = 0
        for sales in best_sales_month:
            if sales['sales_time'] < month_intervals[i]:
                count_for_month_qty += sales['quantite']
                count_for_month_rev += sales['revenue']

        for user_time in customer_month:
            if user_time < month_intervals[i]:
                count_for_month_cust += 1
        total_month.append([count_for_month_qty, count_for_month_rev, count_for_month_cust])

    total_year = []
    for i in range(6):
        count_for_year_qty = 0
        count_for_year_rev = 0
        count_for_year_cust = 0
        for sales in best_sales_year:
            if sales['sales_time'] < year_intervals[i]:
                count_for_year_qty += sales['quantite']
                count_for_year_rev += sales['revenue']

        for user_time in customer_year:
            if user_time < year_intervals[i]:
                count_for_year_cust += 1

        total_year.append([count_for_year_qty, count_for_year_rev, count_for_year_cust])

    final_total = [
        total_day,
        total_month,
        total_year,
        [str(time) for time in day_intervals],
        [str(time) for time in month_intervals],
        [str(time) for time in year_intervals]]
    return final_total


# def stats_chart():

class FlickrAPICustom(FlickrAPI):

    @authenticator
    def authenticate_via_browser(self, perms='read'):
        if isinstance(perms, six.binary_type):
            perms = six.u(perms)

        self.flickr_oauth.get_request_token(oauth_callback='http://' + SITE_HOSTNAME)
        self.flickr_oauth.auth_via_browser(perms=perms)
        token = self.flickr_oauth.get_access_token()
        print(token)
        self.token_cache.token = token

    def get_request_token(self, oauth_callback='http://' + SITE_HOSTNAME + 'flickr_callback', ):
        self.flickr_oauth.get_request_token(oauth_callback=oauth_callback)
