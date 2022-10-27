from django.urls import path
from .views import HpmeQRCode

urlpatterns = [
    path('', HpmeQRCode.as_view(), name='code'),
    
]