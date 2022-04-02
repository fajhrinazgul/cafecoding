from django.urls import path 
from account import views 

app_name = "account"
urlpatterns = [
    path("register/", views.RegisterAccountFormView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("check-username/", views.check_username, name="check_username"),
]