from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext
from django.views import generic
from django.contrib.auth.models import User 
from django.http import HttpResponse, Http404

from rooms.models import Room

class IndexView(generic.ListView):
    """Halaman Utama

    Args:
        generic (_type_): _description_
    """
    template_name = "rooms/index.html"
    model = Room
    context_object_name = "rooms"
    is_index_active = True
    
    def get_queryset(self):
        return Room.objects.filter(is_active=True).order_by("created")
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, gettext(
                f"Silahkan login terlebih dahulu sebelum melanjutkan ke halaman utama <b>Kafe Koding</b>."
            ))
            return redirect("account:login")
        return render(request, self.template_name, {self.context_object_name: self.get_queryset(),
                                                    "is_index_active": self.is_index_active})

class RoomDetailView(generic.DetailView):
    """Halaman detail tentang kelas

    Args:
        generic (_type_): _description_
    """
    template_name = "rooms/room.html"
    model = Room
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rooms"] = Room.objects.all()
        context["is_room_active"] = True # Active Web
        return context

def join_room(request, pk, username):
    """Fungsi untuk membuat pengguna bergabung ke dalam kelas

    Args:
        request (_type_): _description_
        pk (_type_): _description_
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    print(pk)
    print(username)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("<h1>Pengguna Tidak Terdaftar</h1>")
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return HttpResponse("<h1>Pengguna Tidak Terdaftar</h1>")
    if user in room.member.all():
        # Jika pengguna telah bergabung ke dalam grub kelas
        messages.error(request, gettext(
            f"Mohon maaf anda sudah bergabung ke dalam kelas ini."
        ))
    else:
        room.member.add(user)
        room.save()
        messages.success(request, gettext(
            f"Terima kasih, anda telah berhasil bergabung di kelas ini."
        ))
    return redirect(f"/room/{room.slug}/#content")

def quit_room(request, pk, username):
    """Fungsi untuk membuat pengguna keluar dari kelas

    Args:
        request (_type_): _description_
        pk (_type_): _description_
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    print(pk)
    print(username)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("<h1>Pengguna Tidak Terdaftar</h1>")
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return HttpResponse("<h1>Pengguna Tidak Terdaftar</h1>")
    if user in room.member.all():
        # Jika pengguna telah bergabung ke dalam grub kelas
        # Maka bisa dikeluarkan.
        room.member.remove(user)
        room.save()
        messages.success(request, gettext(
            f"Anda telah berhasil keluar dari kelas ini."
        ))
    else:
        messages.error(request, gettext(
            f"Mohon maaf, anda belum bergabung. Bagaimana bisa dikeluarkan hahahaha"
        ))
    return redirect(f"/room/{room.slug}/#content")
