from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.



class MyQrCode(models.Model):
    name = models.CharField(max_length=40,)
    qr_code = models.ImageField(upload_to='qrcode/', blank=True)
    image = models.ImageField(upload_to='profile/')
    
    def __str__(self) :
        return self.name
    
    def save(self,*args, **kwargs):
        qrcode_image = qrcode.make(self.name)
        im = Image.open(self.image)
        im = im.convert("RGBA")
        logo = Image.open(self.image)
        canvas = Image.new('RGB', (290,290),'white')
        #draw = ImageDraw(canvas)
        region = logo
        box = (135,135,235,235)
        region = region.resize((box[2] - box[0], box[3] - box[1]))
        im.crop(box)
        canvas.paste(qrcode_image)
        canvas.paste(region)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        
        im.paste(region,box)
        #im.show()
        
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        
        super().save(*args, **kwargs)