from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext
from django.views import generic
from django.http import JsonResponse

from account.forms import RegisterAccount

class RegisterAccountFormView(generic.FormView):
    """For render forms to html

    Args:
        generic (_type_): _description_
    """
    template_name = "account/register.html"
    form_class = RegisterAccount
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("rooms:index")
        else:
            return render(request, self.template_name, {"form": self.form_class})
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, gettext(
            f"Selamat akun dengan nama pengguna <b>{self.request.POST['username']}</b> berhasil didaftarkan. "
            f"Silahkan lanjutkan ke proses login pada halaman berikut ini. Terimakasih!!!"
        ))
        return redirect("account:login")
    
    def form_invalid(self, form):
        messages.warning(self.request, gettext(
            f"Opps!!! Ada suatu masalah saat mendaftarkan akun Anda. "
        ))
        return redirect("account:register")
    
class LoginView(generic.View):
    """For render login to html

    Args:
        generic (_type_): _description_
    """
    template_name = "account/login.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("rooms:index")
        else:
            return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticated user password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, gettext("Selamat datang kembali di website Kafe Koding"))
            return redirect("rooms:index")
        else:
            messages.error(request, gettext(
                f"Mohon maaf kata sandi yang anda masukkan salah. Silahkan ulangi lagi atau daftar terlebih dahulu "
                f"di halaman <a href='/account/register/' class='alert-link'>pendaftaran.</a>"
            ))
            return render(request, self.template_name)
        
def logout_user(request):
    """For logout user

    Args:
        request (_type_): _description_
    """
    logout(request)
    return redirect("account:login")

def check_username(request):
    if request.method == "POST":
        username = request.POST["username"]
        user = User.objects.get(username=username)
        if user is not None:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(True, safe=False)