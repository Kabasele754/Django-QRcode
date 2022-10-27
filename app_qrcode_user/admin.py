from django.contrib import admin
from .models import ClientUser, CustomerUser
from django.utils.html import format_html

# Register your models here.

# Model Admin room and booking
@admin.register(CustomerUser)
class CLientUserAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="50" />'.format(obj.profile_image.url))

    image_tag.short_description = 'Profile Image'
    list_display = ('name','email','image_tag')

