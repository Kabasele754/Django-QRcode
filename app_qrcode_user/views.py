from django.contrib import messages
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.contrib.auth import  login, logout
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView,View, CreateView

from .models import ClientUser, CustomerUser
from .form import ClientUserForm
from .EmailBackend import EmailBackend

# Create your views here.

class Home(TemplateView):
    template_name = "user/home.html"

# Add Client
class AddClient(View):
    model = ClientUser
    template_name = "user/add_client.html"
    form_class = ClientUserForm
    

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        client_form = self.form_class(request.POST or None, request.FILES or None)
        context = {'form': client_form, 'page_title': 'Add Admin'}
        if request.method == 'POST':
            if client_form.is_valid():
                name = client_form.cleaned_data.get('name')
                email = client_form.cleaned_data.get('email')
                password = client_form.cleaned_data.get('password')

                passport = request.FILES['profile_image']
                fs = FileSystemStorage()
                filename = fs.save(passport.name, passport)
                passport_url = fs.url(filename)
                try:
                    user = CustomerUser.objects.create_user(
                        email=email,type_user=1, name=name,
                        password=password,profile_image=passport_url)
                    user.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('add-client'))
                except Exception as e:
                    messages.error(request, "Could Not Add: " + str(e))
            else:
                messages.error(request, "Could Not Add: ")
        return render(request, self.template_name, context)
    

@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomerUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("/"))
       
        else:
            return redirect(reverse("/"))
    return render(request, 'user/login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.type_user == '1':
                return redirect(reverse("/"))
            else:
                return redirect(reverse("/"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")