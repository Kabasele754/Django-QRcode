from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HpmeQRCode(TemplateView):
    template_name= "home_qrcode.html"
