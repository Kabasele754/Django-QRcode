from django.shortcuts import render
from django.views.generic import TemplateView
from .models import MyQrCode

# Create your views here.


class HpmeQRCode(TemplateView):
    template_name= "home_qrcode.html"
    
    def get_context_data(self, **kwargs):
        context = super(HpmeQRCode, self).get_context_data(**kwargs)
        context['my_qrcode'] = MyQrCode.objects.all()
        
        return context
