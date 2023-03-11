from django.shortcuts import render, redirect
from Applink.forms import *
from DashBoard.Manage import get_tables, decorator_dashboard, decorator_dashboard_ext
from ProdApp.forms import ProduitForm, CategorieForm, SousCategorieForm
from home.Manage import verify_user
from .Manage import *
from dateutil.relativedelta import relativedelta


# Create your views here.
# @decorator_dashboard
def dashboard(request):
    user = verify_user(request)["user"]
    recent_sales_day = get_recent_sales()[2]
    best_sellers_product = get_best_sellers_time()[1]

    get_sales = {'sales': stats_sales()[0][0], 'percent': stats_sales()[0][1]}
    get_revenue = {'revenue': stats_revenu()[1][0], 'percent': stats_revenu()[1][1]}
    get_customer = {'customer': stats_customer()[2][0], 'percent': stats_customer()[2][1]}

    print(timezone.now())
    print(timezone.now() + relativedelta(days=1))

    context = {
        'user': user,
        'top_selling': best_sellers_product,
        'recent_sales': recent_sales_day,
        'get_sales': get_sales,
        'get_revenue': get_revenue,
        'get_customer': get_customer,
    }

    return render(request, 'DashBoard/index.html', context)


@decorator_dashboard
def page_register(request):
    user = verify_user(request)["user"]
    if user is not None:
        return redirect('dash')
    register_admin_form = RegisterForm()

    context = {'register_form': register_admin_form,
               'user': user,
               }

    return render(request, 'DashBoard/pages-register.html', context)


def page_login(request):
    user = verify_user(request)["user"]
    if user is not None:
        return redirect('dash')
    login_admin_form = LoginForm()

    context = {'login_form': login_admin_form,
               'user': user,
               }

    return render(request, 'DashBoard/pages-login.html', context)


@decorator_dashboard
def page_profile(request):
    user = verify_user(request)["user"]
    if not user:
        return redirect('login_admin')

    change_password_form = ChangeForm()
    update_profil_form = UpdateForm(user)

    context = {'user': user,
               'change_form': change_password_form,
               'update_form': update_profil_form,
               }

    return render(request, 'DashBoard/users-profile.html', context)


# @decorator_dashboard_ext
def dashboard_tables(request, intitule):
    user = verify_user(request)["user"]
    context = {}
    context['user'] = user
    if intitule == 'user':
        table = get_tables(request)['data_users']

        context['table'] = table
        context['type'] = 'user'

        return render(request, 'DashBoard/tables-data.html', context)
    if intitule == 'categorie':
        table = get_tables(request)['data_categories']

        context['table'] = table
        context['type'] = 'categorie'

        return render(request, 'DashBoard/tables-data.html', context)

    if intitule == 'sous_categorie':
        table = get_tables(request)['data_sousCategories']

        context['table'] = table
        context['type'] = 'sousCategorie'

        return render(request, 'DashBoard/tables-data.html', context)

    if intitule == 'product':
        table = get_tables(request)['data_products']

        context['table'] = table
        context['type'] = 'product'

        return render(request, 'DashBoard/tables-data.html', context)

    if intitule == 'review':
        table = get_tables(request)['data_reviews']

        context['table'] = table
        context['type'] = 'review'

        return render(request, 'DashBoard/tables-data.html', context)

    if intitule == 'commande':
        table = get_tables(request)['data_commandes']

        context['table'] = table
        context['type'] = 'commande'

        return render(request, 'DashBoard/tables-data.html', context)

    return render(request, 'DashBoard/tables-data.html', context)


# @decorator_dashboard_ext
def dashboard_forms(request, intitule):
    user = verify_user(request)["user"]
    context = {}
    context['user'] = user

    if intitule == 'user':
        form = RegisterForm()

        context['form'] = form
        context['type'] = 'user'

        return render(request, 'DashBoard/forms-data.html', context)

    if intitule == 'product':
        form = ProduitForm()

        context['form'] = form
        context['type'] = 'product'

        return render(request, 'DashBoard/forms-data.html', context)
    if intitule == 'categorie':
        form = CategorieForm()

        context['form'] = form
        context['type'] = 'categorie'

        return render(request, 'DashBoard/forms-data.html', context)

    if intitule == 'sous_categorie':
        form = SousCategorieForm()

        context['form'] = form
        context['type'] = 'sousCategorie'

        return render(request, 'DashBoard/forms-data.html', context)

    return render(request, 'DashBoard/forms-data.html', context)


# @decorator_dashboard_ext
def dashboard_forms_update(request, intitule, id):
    user = verify_user(request)["user"]
    context = {}
    context['user'] = user

    if intitule == 'user':
        id = str(id)
        id = id.replace('-', '')
        user = Utilisateurs.objects.get(pk=id)
        form = UpdateForm(instance=user)

        context['form'] = form
        context['type'] = 'user'

        return render(request, 'DashBoard/forms-update-data.html', context)

    if intitule == 'product':
        id = str(id)
        id = id.replace('-', '')
        product = Produit.objects.get(pk=id)
        form = ProduitForm(instance=product)

        context['form'] = form
        context['type'] = 'product'
        context['id'] = id

        return render(request, 'DashBoard/forms-update-data.html', context)
    if intitule == 'categorie':
        id = str(id)
        id = id.replace('-', '')
        categorie = Categorie.objects.get(pk=id)
        form = CategorieForm(instance=categorie)

        context['form'] = form
        context['type'] = 'categorie'

        return render(request, 'DashBoard/forms-update-data.html', context)

    if intitule == 'sous_categorie':
        id = str(id)
        id = id.replace('-', '')
        sous_categorie = SousCategorie.objects.get(pk=id)
        form = SousCategorieForm(instance=sous_categorie)

        context['form'] = form
        context['type'] = 'sousCategorie'

        return render(request, 'DashBoard/forms-update-data.html', context)

    return render(request, 'DashBoard/forms-update-data.html', context)
