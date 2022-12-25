from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from EShopGTI import settings
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('all_product', views.category, name="category"),
    path('product/<id>', views.product, name='product'),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('link_valid', views.LinkValidation, name='linkvalid'),
    re_path(r'^google-login/$', views.google_login, name="google_login"),
    re_path("thankyou/(?P<user>)",views.thankregistration,name='thankyou'),
    path("updateuser", views.update_user, name="update_user"),
    path('profil', views.profil, name='my_profil'),
    path('logout', views.logout_user, name=""),
    path('delete', views.delete_user, name=''),
    path('filling', views.fill, name='fill' ),
    path('passordUserChange', views.password_change, name='pass'),
    path('activate/?P<uidb64>/?P<token>', views.activate, name='activate' ),
    path('cartdetail', views.cart, name='cart'),
    path('wishlist' , views.wishlist, name='wishlist'),
    path('test', views.test),
    path('invoice', views.invoice_order, name='invoice'),
    path('refresh/?P<uidb64>/?P<token>', views.activate_forgout, name='refresh_password'),
    path('forgotpassword', views.forgout_pass, name='forgot_render'),
    path('shipping', views.shipping, name='shipping'),
    path('search', views.search_product, name='search_product'),
    path('retrieve_categorie/<id>', views.retrieve_categorie, name='retrieve_categorie'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)