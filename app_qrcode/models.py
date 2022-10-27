from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.



class MyQrCode(models.Model):
    name = models.CharField(max_length=40,)
    qr_code = models.ImageField(upload_to='qrcode/')
