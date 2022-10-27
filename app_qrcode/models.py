from turtle import fillcolor
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
        # get my image 
        im = Image.open(self.image)
        im = im.convert("RGBA")
        logo = Image.open(self.image)
        # Size image
        base_with = 75
        wpercent = (base_with / float(logo.size[0]))
        hsize = int((float(logo.size[1])* float(wpercent)))
        logo = logo.resize((base_with, hsize), Image.ANTIALIAS)
        qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        # Add my name
        qr_big.add_data(self.name)
        qr_big.make(fit=True)
        
        img_qr_big = qr_big.make_image(fill_color="black", back_color = "white").convert("RGB")
        # update the position image
        pos = ((img_qr_big.size[0]- logo.size[0])//2,(img_qr_big.size[1]- logo.size[1])//2)
        canvas = Image.new('RGB', (290,290),'white')
        
       
        img_qr_big.paste(logo, pos)
        canvas.paste(img_qr_big)
        
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        
        
        # save the image in variable qr_code
        
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        
        super().save(*args, **kwargs)