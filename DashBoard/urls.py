from django.urls.conf import path, re_path
from .views import *
from django.conf.urls.static import static
from EShopGTI import settings

urlpatterns = [

    path('dashboard', dashboard, name='dash'),
    path('register', page_register, name='register_admin'),
    path('login', page_login, name='login_admin'),
    path('profile', page_profile, name='profile'),
    path('tables/<intitule>', dashboard_tables, name='dash_tables'),
    path('forms/<intitule>', dashboard_forms,name='dash_forms'),
    path('formsupdate/<intitule>/<id>', dashboard_forms_update, name='dash_forms_update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)