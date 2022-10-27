from dataclasses import fields
from socket import fromshare
from symbol import import_stmt
from django import forms
from .models import CustomerUser, ClientUser
from django.core.exceptions import ValidationError

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class CustomerUserForm(FormSettings):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)    
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }

    profile_image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomerUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomerUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomerUserForm.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomerUserForm.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomerUser
        fields = ['nom', 'postnom', 'email', 'genre','profile_image',]


class ClientUserForm(CustomerUserForm):
    def __init__(self, *args, **kwargs):
        super(ClientUserForm, self).__init__(*args, **kwargs)

    class Meta(CustomerUserForm.Meta):
        model = ClientUser
        fields = CustomerUserForm.Meta.fields
