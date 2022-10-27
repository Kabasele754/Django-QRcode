from django.urls import path
from .views import Home, AddClient,check_email_availability, login_page, doLogin, logout_user

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # for login and logout
    path("login/", login_page, name='login'),
    path("doLogin/", doLogin, name='user_login'),
    path("logout_user/", logout_user, name='user_logout'),
    # for to add  client user
    path('add-client', AddClient.as_view(), name='add-client'),
     path("check_email_availability", check_email_availability,
         name="check_email_availability"),
]