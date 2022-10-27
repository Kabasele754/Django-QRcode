from django.db import models

# Create your models here.



class MyQrCode(models.Model):
    name = models.CharField(max_length=40,)
