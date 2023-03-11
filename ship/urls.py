from django.urls.conf import path
from .views import scan_verify


urlpatterns = [
    path('scan_verify', scan_verify, name='scan_verify'),
]