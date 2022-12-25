import json
from django.http import FileResponse
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.files import File
from django.db import transaction

from DashBoard.Manage import get_best_sellers_time, stats_customer, stats_revenu, stats_sales, stats_chart
from EShopGTI.settings import SITE_HOSTNAME
from home.Manage import verify_user
from .generate import generate_invoice
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from home.models import *
from rest_framework.response import Response
import qrcode

from .document import DocumentProduit
from .serializer import *
from elasticsearch_dsl import Q


@api_view(["GET"])
def Produit_all(request):
    all_produit = []
    error_produit = []
    produit = Produit.objects.all()
    for pr in produit:
        produit_serializer = ProduitSerializer(pr)
        if produit_serializer.is_valid():
            all_produit += [produit_serializer.data]
        else:
            error_produit += [produit_serializer.errors]
    if len(all_produit) == len(produit):
        return Response(all_produit)
    else:
        return Response(error_produit)


# @api_view(["GET",])
# def product_retrieve(request):


@csrf_exempt
@api_view(["GET", ])
def Add_to_cart(request):
    user = Utilisateurs.objects.get(pk=request.session["user_primary"])
    cart, _ = Panier.objects.get_or_create(utilisateur=user)
    cart.save()

    id_produit = str(request.GET['id_produit'])
    id_produit = id_produit.replace('-', '')
    produit = Produit.objects.get(pk=id_produit)
    if produit in cart.produit_set.all():

        pr = PanierProduit.objects.get(panier=cart, product=produit)
        if request.GET.get('quantite'):
            pr.__dict__.update({"quantite": int(pr.quantite) + int(request.GET.get('quantite'))})
        else:
            pr.__dict__.update({"quantite": int(pr.quantite) + 1})
        pr.save()
    else:
        if request.GET.get('quantite'):
            produit.panier.add(cart)
            produit.save()
            pr_insave = PanierProduit.objects.get(panier=cart, product=produit)
            pr_insave.__dict__.update({"quantite": int(request.GET.get('quantite'))})
            pr_insave.save()
        else:
            produit.panier.add(cart)
            produit.save()

    cart_number = len(cart.produit_set.all())

    request.session["cart_count"] = cart_number

    return Response({"cart_number": cart_number}, status=200)


@api_view(["GET", ])
def Delete_to_cart(request):
    produit = Produit.objects.get(pk=request.GET['id_produit'])
    user = Utilisateurs.objects.get(pk=request.session['user_primary'])
    cart = Panier.objects.get(utilisateur=user)

    produit.panier.remove(cart)

    produit.save()

    cart_number = len(cart.produit_set.all())

    return Response({"cart_number": cart_number}, status=200)


@api_view(["GET"])
def cart_number_return(request):
    user = Utilisateurs.objects.get(pk=request.session['user_primary'])
    cart = Panier.objects.get(utilisateur=user)

    cart_number = len(cart.produit_set.all())

    return Response({'cart_total': cart_number}, status=200)


@api_view(["GET"])
def Update_to_cart(request):
    user = Utilisateurs.objects.get(pk=request.session['user_primary'])
    cart = Panier.objects.get(utilisateur=user)

    list_update = request.GET
    print(request.GET)

    for key in list_update:
        for cle, valeur in json.loads(key).items():
            print(valeur)
            val_1 = valeur['id'].replace('-', '')
            val_2 = int(valeur['qte'])

            produit = Produit.objects.get(pk=val_1)
            produit_in_cart = PanierProduit.objects.get(panier=cart, product=produit)
            produit_in_cart.__dict__.update({"quantite": val_2})

            produit_in_cart.save()

    return Response(status=200)


@api_view(["GET"])
def Add_to_wishlist(request):
    user = Utilisateurs.objects.get(pk=request.session["user_primary"])
    wishlist, _ = Favoris.objects.get_or_create(utilisateur=user)
    wishlist.save()

    id_produit = str(request.GET['id_produit'])
    id_produit = id_produit.replace('-', '')
    produit = Produit.objects.get(pk=id_produit)
    if produit in wishlist.produit_set.all():
        return Response(status=400)
    else:

        produit.favoris.add(wishlist)
        produit.save()

        wishlist_number = len(wishlist.produit_set.all())

        request.session["wishlist_count"] = wishlist_number

        return Response({"wishlist_number": wishlist_number}, status=200)


@api_view(["GET", ])
def Delete_to_wishlist(request):
    produit = Produit.objects.get(pk=request.GET['id_produit'])
    user = Utilisateurs.objects.get(pk=request.session['user_primary'])
    wishlist = Favoris.objects.get(utilisateur=user)

    produit.favoris.remove(wishlist)

    produit.save()

    wishlist_number = len(wishlist.produit_set.all())

    return Response({"wishlist_number": wishlist_number}, status=200)


@api_view(['GET', 'POST'])
@transaction.atomic
def Command_product(request):
    ship_price = {'Free Shipping': 0, 'Standart Shipping': 10, 'Express Shipping': 20}
    user = Utilisateurs.objects.get(pk=request.session['user_primary'])
    user_cart = Panier.objects.get(utilisateur=user)
    prix_total = 0
    try:
        ship_session = request.session['ship_option']
    except:
        ship_session = None

    if ship_session == 'No Option':
        ship_session = 'Free Shipping'

    if request.method == 'POST':
        livraison = LivraisonSerializer(data=request.data)
        if livraison.is_valid():
            print(request.data)
            my_livraison = livraison.perform_save(livraison.validated_data)

            all_product_cart = user_cart.produit_set.all()
            commande = Commandes.objects.create(utilisateur=user, livraison=my_livraison, date_livraison=None)
            commande.save()
            for product in all_product_cart:
                product_quantite = PanierProduit.objects.get(panier=user_cart, product=product).quantite
                print(product_quantite)

                if product.stock > product_quantite:

                    product.__dict__.update({'stock': product.stock - product_quantite})
                    product.save()
                    product.commande.add(commande)
                    product.save()

                    product_command = CommandeProduit.objects.get(commande=commande, produit=product)
                    product_command.__dict__.update({'quantite': product_quantite})
                    product_command.save()
                    prix_total += product_quantite * product.prix
                else:
                    pass

            print(prix_total)
            price_updated = prix_total + ship_price[ship_session]
            commande.__dict__.update({'prix_total': price_updated, 'ship_option': ship_session})
            commande.save()

            return Response(model_to_dict(commande), status=200)

        else:

            return Response(livraison.errors, status=400)
    else:
        return Response(status=401)


@api_view(['GET'])
@transaction.atomic
def command_instance(request, user):
    user = Utilisateurs.objects.get(pk=user)
    commande = Commandes.objects.filter(utilisateur=user).order_by('-date_commande')
    if len(commande) != 0:

        commande_instance = commande[0]
        invoice_id = str(commande_instance.pk)
        invoice_id = "#00" + invoice_id[0:3:1]
        valide = commande_instance.valide
        pending = commande_instance.pending

        livraison = commande_instance.livraison
        livraison = model_to_dict(livraison)
        products_commande = commande_instance.produit_set.all()
        produits_list = []
        total_commande = 0
        for product in products_commande:
            product_id = str(product.pk)
            product_id = "#500" + product_id[0:3:1]

            quantity = CommandeProduit.objects.get(produit=product, commande=commande_instance).quantite
            subtotal = product.prix * quantity
            produits_list.append(
                {'product_id': product_id, 'name': product.nom, 'quantite': quantity, 'subtotal': subtotal})

            total_commande += subtotal
        month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Otobre',
                 'Novembre', 'Decembre']
        date_commande = commande_instance.date_commande
        date_commande = str(date_commande.day) + ' ' + str(month[date_commande.month - 1]) + ' ' + str(
            date_commande.year)

        invoice_details = {'commande_id': str(commande_instance.pk),
                           'invoice_id': invoice_id,
                           'livraison': livraison,
                           'products': produits_list,
                           'date_commande': date_commande,
                           'total': total_commande,
                           'valide': valide,
                           'pending': pending,
                           'ship_option': commande.ship_option}

        return Response(invoice_details, status=200)
    else:
        return Response(status=400)


@api_view(['GET', 'POST'])
@transaction.atomic
def comment_product(request):
    user = Utilisateurs.objects.get(pk=request.session['user_primary'])
    id = request.data['produit_id']
    id = id.replace('-', '')
    product = Produit.objects.get(pk=id)

    a = request.data['data'].split('&')
    liste = []
    for i in range(1, 3):
        b = a[i].split('=')
        liste.append(b[1])

    data_got = {'contenu': liste[0], 'name': liste[1]}

    review_content = ReviewSerializer(data=data_got)
    if review_content.is_valid():
        try:
            review = Avis.objects.get(utilisateur=user, produit=product)
            review.delete()
        except:
            pass

        review = Avis.objects.create(utilisateur=user, produit=product,
                                     contenu=review_content.validated_data['contenu'],
                                     name=review_content.validated_data['name'], rating=request.data['rate'],
                                     date=timezone.now())
        review.save()

        return Response(model_to_dict(review), status=200)

    else:

        return Response(review_content.errors, status=400)


@api_view(['GET', 'POST'])
def search_product(request):
    # data = {}
    # for product in Produit.objects.all():
    #   data[str(product.pk)] = {'nom': product.nom}

    # print(request.data['search'])
    request.session['search_phrase'] = request.GET['search']

    q = Q(
        'multi_match',
        query=request.GET['search'],

        fields=[
            'nom'
        ])

    search = DocumentProduit.search().query(q)
    response = search.execute()
    print(response)
    dictionaire = []
    search_queryset = search.to_queryset()
    for search_item in search_queryset:
        search_item = ProduitSerializer(data=model_to_dict(search_item))
        if search_item.is_valid():
            dictionaire.append(search_item.data)


    else:
        return Response(dictionaire, status=200)


# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    products = Produit.objects.all()

    data_product = []
    for product in products:

        product_searializer = ProduitSerializer(data=model_to_dict(product))

        if product_searializer.is_valid():
            try:
                qr_code = product.qr_code_file.url
            except:
                qr_code = None

            data_product.append(
                {'product_pk': product.pk, 'product_qr': qr_code, 'product_data': product_searializer.data,
                 'product_categorie': product.categorie.nom})

    return Response({'products': data_product}, status=200)


@api_view(['GET'])
def get_all_categorie(request):
    categories = Categorie.objects.all()

    data_categorie = []
    data_categorie_sous_categorie = []
    first_sous_categorie = None
    data_categorie_sous_categorie_other = None

    for categorie in categories:

        categorie_serializer = CategorieSerializer(data=model_to_dict(categorie))
        its_sous_categorie = SousCategorie.objects.filter(categorie=categorie)
        if len(its_sous_categorie) != 0:
            for sous_categorie in its_sous_categorie:
                data_categorie_sous_categorie.append(model_to_dict(sous_categorie))
        else:
            data_categorie_sous_categorie = []

        if len(data_categorie_sous_categorie) >= 2:
            first_sous_categorie = data_categorie_sous_categorie[0]
            data_categorie_sous_categorie_ext = data_categorie_sous_categorie
            data_categorie_sous_categorie_ext.pop(0)
            data_categorie_sous_categorie_other = data_categorie_sous_categorie_ext

        try:
            image = categorie.image.url
        except:
            image = None

        products_in_category = Produit.objects.filter(categorie=categorie)
        if len(products_in_category) == 0:
            have_product = 0
        else:
            have_product = 1

        if categorie_serializer.is_valid():

            data_categorie.append({'categorie_pk': categorie.pk,
                                   'categorie_image': image,
                                   'categorie_data': categorie_serializer.data,
                                   'its_sous_categorie': data_categorie_sous_categorie,
                                   'len_sous_categorie': len(data_categorie_sous_categorie),
                                   'first_sous_categorie': first_sous_categorie,
                                   'its_sous_categorie_ext': data_categorie_sous_categorie_other,
                                   'have_product': have_product})

        else:
            print(categorie_serializer.errors)
    return Response({'categories': data_categorie}, status=200)


@api_view(['GET'])
def get_all_sousCategories(request):
    sousCategories = SousCategorie.objects.all()

    data_sousCategorie = []

    for sousCategorie in sousCategories:

        sousCategorie_serializer = SousCategorieSerializer_ext(data=model_to_dict(sousCategorie))

        products_in_sousCategorie = Produit.objects.filter(sous_catgeorie=sousCategorie)
        if len(products_in_sousCategorie) == 0:
            have_product = 0
        else:
            have_product = 1

        if sousCategorie_serializer.is_valid():
            data_sousCategorie.append({'sousCategorie_pk': sousCategorie.pk,
                                       'sousCategorie_data': sousCategorie_serializer.data,
                                       'categorie': sousCategorie.categorie.nom,
                                       'have_product': have_product})

    return Response({'sousCategories': data_sousCategorie}, status=200)


@api_view(['GET'])
def get_all_avis(request):
    reviews = Avis.objects.all()

    data_reviews = []

    for review in reviews:

        review_serializer = ShowReviewSerializer(data=model_to_dict(review))

        if review_serializer.is_valid():
            data_reviews.append({'review': review.pk,
                                 'review_data': review_serializer.data,
                                 'review_user': review.utilisateur.first_name + ' ' + review.utilisateur.last_name,
                                 'review_product': review.produit.nom, })

    return Response({'reviews': data_reviews}, status=200)


@api_view(['GET'])
def get_all_commandes(request):
    commandes = Commandes.objects.all()

    data_commande = []

    first_product = None
    data_commande_product_other = None
    # print(len(categories))
    for commande in commandes:
        data_commande_product = []

        commande_serializer = CommandeSerializer(data=model_to_dict(commande))
        its_products = CommandeProduit.objects.filter(commande=commande)

        if len(its_products) != 0:
            for product_get in its_products:
                data_commande_product.append({'nom': product_get.produit.nom, 'quantite': product_get.quantite})
        else:
            pass

        if len(data_commande_product) > 1:
            first_product = data_commande_product[0]
            data_commande_product_ext = data_commande_product.copy()
            data_commande_product_ext.pop(0)
            data_commande_product_other = data_commande_product_ext

        print(first_product)
        if commande_serializer.is_valid():
            data_commande.append({'commande_pk': commande.pk,
                                  'commande_data': commande_serializer.data,
                                  'its_products': data_commande_product,
                                  'len_products': len(data_commande_product),
                                  'first_product': first_product,
                                  'its_products_ext': data_commande_product_other,
                                  'commande_user': commande.utilisateur.first_name + ' ' + commande.utilisateur.last_name,
                                  'commande_livraison': commande.livraison.first_name + ' ' + commande.livraison.last_name + ' ' + commande.livraison.address + ' ' + commande.livraison.city + ' ' + commande.livraison.phone_number})

    return Response({'commandes': data_commande}, status=200)


@api_view(['GET'])
def delete_product(request):
    id = request.GET['id']
    id = str(id)
    id = id.replace('-', '')
    product = Produit.objects.get(pk=id)

    product.delete()

    return Response(status=200)


@api_view(['GET'])
def archive_product(request):
    id = request.GET['id']
    id = str(id)
    id = id.replace('-', '')
    product = Produit.objects.get(pk=id)

    product.__dict__.update({'is_archive': True})

    product.save()

    return Response(status=200)


@api_view(['GET'])
def delete_categorie(request):
    id = request.GET['id']

    categorie = Categorie.objects.get(pk=id)

    categorie.delete()

    return Response(status=200)


@api_view(['GET'])
def delete_sousCategorie(request):
    id = request.GET['id']

    sousCategorie = SousCategorie.objects.get(pk=id)

    sousCategorie.delete()

    return Response(status=200)


@api_view(['GET'])
def delete_commande(request):
    id = request.GET['id']
    id = str(id)
    id = id.replace('-', '')

    commande = Commandes.objects.get(pk=id)

    commande.delete()

    return Response(status=200)


@api_view(['GET', 'POST'])
def add_product(request):
    if request.method == 'POST':

        product_serializer = ProduitSerializer_ext(data=request.data)

        if product_serializer.is_valid():

            get_field_sous_categorie = product_serializer.validated_data['sous_categorie']
            get_field_categorie = product_serializer.validated_data['categorie']
            print(get_field_categorie)
            # got_category = Categorie.objects.get(pk=get_field_categorie)
            # got_sous_categorie = SousCategorie.objects.filter(pk=get_field_sous_categorie)
            got_category_mactch = SousCategorie.objects.filter(categorie=get_field_categorie)
            if get_field_sous_categorie is not None and get_field_sous_categorie not in got_category_mactch:
                return Response({'category_not_exist': 1}, status=400)
            else:

                product = product_serializer.save()
                data = 'http://' + SITE_HOSTNAME + '/product/' + str(product.pk)
                product_code = qrcode.make(data)
                id_of_product = str(product.pk)
                id_of_product = "500" + id_of_product[0:3:1]

                product_code.save('images/qrProduct' + id_of_product + '.png')
                file_path = open('images/qrProduct' + id_of_product + '.png', mode='rb')
                file = File(file_path, name=file_path.name)
                product.__dict__.update({'qr_code_file': file})
                product.save()

            return Response(product_serializer.data, status=200)
        else:
            return Response(product_serializer.errors, status=400)


@api_view(['GET', 'POST'])
def add_categorie(request):
    if request.method == 'POST':

        data_got = {'image': request.FILES['image'],
                    'nom': request.data['nom']}
        # print(request.data)
        categorie_serializer = CategorieSerializer_ext(data=request.data)

        if categorie_serializer.is_valid():

            categorie_serializer.save()
            # print(request.FILES['image'])
            # print(categorie_serializer.validated_data)
            # print(categorie_serializer.data)

            return Response(categorie_serializer.data, status=200)
        else:
            return Response(categorie_serializer.errors, status=400)


@api_view(['GET', 'POST'])
def add_sousCategorie(request):
    if request.method == 'POST':
        sousCategorie_serializer = SousCategorieSerializer(data=request.data)

        if sousCategorie_serializer.is_valid():

            print(sousCategorie_serializer.data)

            sousCategorie_serializer.perform_save(sousCategorie_serializer.validated_data)

            return Response(sousCategorie_serializer.data, status=200)
        else:
            return Response(sousCategorie_serializer.errors, status=400)


@api_view(['POST'])
def update_product(request):
    product = Produit.objects.get(pk=request.data['id'])
    if request.method == 'POST':

        update_serializer = ProduitSerializer(data=request.data['data'])

        if update_serializer.is_valid():

            update_serializer.save()

            product.__dict__.update(update_serializer.data)

            product.save()

            return Response(update_serializer.data, status=200)
        else:
            return Response(update_serializer.errors, status=400)


@api_view(['POST'])
def update_categorie(request):
    categorie = Categorie.objects.get(pk=request.data['id'])
    if request.method == 'POST':

        update_serializer = CategorieSerializer(data=request.data['data'])

        if update_serializer.is_valid():

            update_serializer.save()

            categorie.__dict__.update(update_serializer.data)

            categorie.save()

            return Response(update_serializer.data, status=200)
        else:
            return Response(update_serializer.errors, status=400)


@api_view(['POST'])
def update_sousCategorie(request):
    sousCategorie = SousCategorie.objects.get(pk=request.data['id'])
    if request.method == 'POST':

        update_serializer = SousCategorieSerializer(data=request.data['data'])

        if update_serializer.is_valid():

            update_serializer.save()

            sousCategorie.__dict__.update(update_serializer.data)

            sousCategorie.save()

            return Response(update_serializer.data, status=200)
        else:
            return Response(update_serializer.errors, status=400)


@api_view(['GET'])
def vaidate_commande(request):
    ship_option = {'Free Shipping': 0, 'Standart Shipping': 10, 'Express Shipping': 20}
    id = request.GET['id']
    id = str(id)
    id = id.replace('-', '')
    commande = Commandes.objects.get(pk=id)
    commande.__dict__.update({'valide': 1})
    commande.save()
    invoice_id = str(commande.pk)
    invoice_id = "#00" + invoice_id[0:3:1]
    data_qr_code = "Green Tech Innovation. Commande No " + invoice_id + "  verifie au nom de " + \
                   model_to_dict(commande.utilisateur)['first_name'] + " " + model_to_dict(commande.utilisateur)[
                       'last_name']
    qr_code = qrcode.make(data_qr_code)
    making_id = str(invoice_id).replace('#', '')
    qr_code.save('images/qr/qrcode' + making_id + '.png')
    qr_file_path = 'images/qr/qrcode' + making_id + '.png'
    option_for_commande = commande.ship_option
    price_principal = commande.prix_total - ship_option[option_for_commande]
    data_invoice = {'id': invoice_id,
                    'livraison': model_to_dict(commande.livraison),
                    'user': model_to_dict(commande.utilisateur),
                    'products': [],
                    'all_total': price_principal,
                    'date': str(commande.date_commande.day) + "/" + str(commande.date_commande.month) + '/' + str(
                        commande.date_commande.year),
                    'file_qrcode': qr_file_path,
                    'ship_option': commande.ship_option,
                    'ship_price': ship_option[option_for_commande],
                    }

    for product in commande.produit_set.all():
        product_id = str(product.pk)
        product_id = "#500" + product_id[0:3:1]
        quantite = CommandeProduit.objects.get(produit=product, commande=commande).quantite

        data_invoice['products'].append({'id': product_id,
                                         'name': product.nom,
                                         'price': product.prix,
                                         'quantity': quantite,
                                         'total': product.prix * quantite,
                                         }
                                        )

    try:
        gone_well = True
        file = File(generate_invoice(data_invoice), name=generate_invoice(data_invoice).name)
        facture = Facture.objects.create(commande=commande,
                                         utilisateur=commande.utilisateur,
                                         total=commande.prix_total,
                                         source=file)
        facture.save()
    except Exception as e:

        gone_well = False

        print(e)

    return Response(status=200)


@api_view(['GET'])
def mark_livrate(request):
    id = request.GET['id']
    id = str(id)
    id = id.replace('-', '')

    commande = Commandes.objects.get(pk=id)

    commande.__dict__.update({'livree': 1, 'date_livraison': timezone.now()})

    commande.save()

    return Response(status=200)


@api_view(['GET'])
def download_invoice(request, id):
    user = verify_user(request)['user']
    if user is not None:
        commande_id = str(id)
        commande_id = commande_id.replace('-', '')
        commande = Commandes.objects.get(pk=commande_id)

        facture = Facture.objects.get(commande=commande)
        invoice_file = facture.source
    else:
        return redirect('home')

    return FileResponse(invoice_file.open(), as_attachment=True)


@api_view(['GET'])
def download_qr(request, id):
    product_id = str(id)
    product_id = product_id.replace('-', '')
    product = Produit.objects.get(pk=product_id)

    product_qr = product.qr_code_file

    return FileResponse(product_qr.open(), filename=product.nom + '.png', as_attachment=True)


@api_view(['GET'])
@transaction.atomic
def save_shipping_option(request):
    get_user = verify_user(request)['user']
    products_cannot_by = []
    if get_user is not None:
        get_user_object = Utilisateurs.objects.get(email=get_user['email'])
        get_cart_object = Panier.objects.get(utilisateur=get_user_object)
        for product in get_cart_object.produit_set.all():
            quantity_in_cart = PanierProduit.objects.get(panier=get_cart_object, produit=product).quantite
            product_quantite = product.stock
            if product_quantite < quantity_in_cart:
                products_cannot_by.append(product.nom)
        if len(products_cannot_by) != 0:
            return Response(products_cannot_by, status=400)
        else:
            shipping_option = request.GET['shipping_option']
            request.session['shipping_option'] = shipping_option

    return Response(status=200)


@api_view(['GET'])
def best_sellers_time(request):
    data = []
    time = request.GET['time']
    if time == 'day':
        data = get_best_sellers_time()[0]
    if time == 'month':
        data = get_best_sellers_time()[1]
    if time == 'year':
        data = get_best_sellers_time()[2]

    return Response(data, status=200)


@api_view(['GET'])
def stats_best_sales(request):
    data = []
    time = request.GET['time']

    if time == 'day':
        data = stats_sales()[0]
    if time == 'month':
        data = stats_sales()[1]
    if time == 'year':
        data = stats_sales()[2]

    return Response(data, status=200)


@api_view(['GET'])
def stats_best_revenu(request):
    data = []
    time = request.GET['time']

    if time == 'day':
        data = stats_revenu()[0]
    if time == 'month':
        data = stats_revenu()[1]
    if time == 'year':
        data = stats_revenu()[2]

    return Response(data, status=200)


@api_view(['GET'])
def stats_best_customer(request):
    data = []
    time = request.GET['time']

    if time == 'day':
        data = stats_customer()[0]
    if time == 'month':
        data = stats_customer()[1]
    if time == 'year':
        data = stats_customer()[2]

    return Response(data, status=200)


@api_view(['GET'])
def stats_chart_api(request):
    data = []
    time = request.GET['time']

    if time == 'day':
        sales = []
        rev = []
        cust = []
        for _instance in stats_chart()[0]:
            sales.append(_instance[0])
            rev.append(_instance[1])
            cust.append(_instance[2])
        data = {'data': [sales, rev, cust], 'intervals': stats_chart()[3]}

    if time == 'month':
        sales = []
        rev = []
        cust = []
        for _instance in stats_chart()[1]:
            sales.append(_instance[0])
            rev.append(_instance[1])
            cust.append(_instance[2])
        data = {'data': [sales, rev, cust], 'intervals': stats_chart()[4]}

    if time == 'year':
        sales = []
        rev = []
        cust = []
        for _instance in stats_chart()[2]:
            sales.append(_instance[0])
            rev.append(_instance[1])
            cust.append(_instance[2])
        data = {'data': [sales, rev, cust], 'intervals': stats_chart()[5]}

    return Response(data, status=200)
