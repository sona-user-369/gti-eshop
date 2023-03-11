from django.urls.conf import path, re_path
from .views import *

urlpatterns =[

    path('addcart', Add_to_cart, name='add_cart'),
    path('deletcart', Delete_to_cart, name='delete_cart'),
    path('updatecart', Update_to_cart, name='update_cart'),
    path('addwishlist', Add_to_wishlist, name = 'add_wishlist'),
    path('deletewishlist', Delete_to_wishlist, name='delete_wishlist'),
    path('valid_commande', Command_product, name='valid_commande'),
    path('commande/<user>', command_instance, name='commande'),
    path('comment', comment_product, name='comment'),
    path('search', search_product, name='search'),
    path('all_tables_products', get_all_products, name='all_tables_products'),
    path('all_tables_categories', get_all_categorie),
    path('all_tables_sousCategories', get_all_sousCategories),
    path('all_tables_reviews', get_all_avis),
    path('all_tables_commandes', get_all_commandes),
    path('deleteOnProduct', delete_product, name='delete_product'),
    path('deleteOnCategorie', delete_categorie, name='delete_categorie'),
    path('deleteOnSousCategorie', delete_sousCategorie, name='delete_sousCategorie'),
    path('deleteOnCommande', delete_commande, name='delete_commande'),
    path('addproduct', add_product, name='add_product'),
    path('addcategorie', add_categorie, name='add_categorie'),
    path('addsouscategorie', add_sous_categorie, name='add_sousCategorie'),
    path('updateproduct', update_product, name='update_product'),
    path('updatecategorie', update_categorie, name='update_categorie'),
    path('updatesouscategorie', update_sous_categorie, name='update_sousCategorie'),
    path('validatecommande', vaidate_commande, name='validate_commande'),
    path('livratecommande', mark_livrate, name='livrate_commande'),
    path('download/<id>', download_invoice, name='download'),
    path('download_qr/<id>', download_qr, name='download_qr'),
    path('ship_option', save_shipping_option, name='save_ship_option'),
    path('archive_product', archive_product, name='archive_product'),
    path('get_top', best_sellers_time, name='get_top'),
    path('get_sales', stats_best_sales, name='get_sales'),
    path('get_revenue', stats_best_revenu, name='get_revenue'),
    path('get_customer', stats_best_customer, name='get_customer'),
    path('get_chart', stats_chart_api, name='get_chart'),
    path('addcartcookie', add_cart_cookie, name='add_cart_cookie'),
    path('deletecartcookie', delete_cart_cookie, name='delete_cart_cookie'),
    path('update_cart_cookie', update_cart_cookie, name='update_cart_cookie'),
    path('update_to_cart_object', update_to_cart_object, name='update_to_cart_object'),
    path('add_wishlist_cookie', add_wishlist_cookie, name='add_wishlist_cookie'),
    path('delete_wishlist_cookie', delete_wishlist_cookie, name='delete_wishlist_cookie'),
    path('update_to_wishlist_object', update_to_wishlist_object, name='update_to_wishlist_object'),

    # path('flickr_callback', flickr_callback, name='flickr_callback'),




]