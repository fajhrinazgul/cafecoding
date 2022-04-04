from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.translation import gettext
from django.views import generic
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.db.models import Q 
from functools import reduce
import operator

from rooms.forms import RoomEditForm

from rooms.models import Room

class IndexView(generic.ListView, LoginRequiredMixin):
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

class RoomDetailView(generic.DetailView, LoginRequiredMixin):
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

class RoomSearchListView(generic.ListView, LoginRequiredMixin):
    """Render pencarian

    Args:
        generic (_type_): _description_
    """
    template_name = "rooms/search.html"
    context_object_name = "rooms"
    is_index_active = True
    
    def get_queryset(self):
        """Pencarian
        """
        query = self.request.GET.get("q")
        
        if query:
            query_list = query.split()
            search_result = Room.objects.filter(
                reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(content__icontains=q) for q in query_list))
            )
            
            if not search_result:
                # Jika pencarian tidak ditemukan
                messages.info(self.request, gettext(
                    f"Tidak ada hasil untuk pencarian <b>{query}</b>"
                ))
                return search_result.filter(is_active=True)
            else:
                # Jika pencarian ditemukan
                messages.success(self.request, gettext(
                    f"Hasil pencarian untuk <b>{query}</b>"
                ))
                return search_result.filter(is_active=True)
        else:
            # Jika mencari dengan query kosong
            messages.error(self.request, gettext(
                f"Maaf keyword tidak boleh kosong."
            ))
            return []
    
    def get_context_data(self, **kwargs):
        context = super(RoomSearchListView, self).get_context_data(**kwargs)
        context["is_index_active"] = self.is_index_active
        return context

class RoomUpdateFormView(generic.UpdateView, LoginRequiredMixin):
    """Fungsi untuk merender agar mentor bisa mengedit room

    Args:
        generic (_type_): _description_
    """
    template_name = "rooms/room_edit.html"
    form_class = RoomEditForm
    model = Room
    
    def form_valid(self, form):
        """Jika form valid maka form akan disimpan

        Args:
            form (_type_): _description_
        """
        form.save()
        room = get_object_or_404(Room, pk=self.kwargs.get("pk"))
        messages.success(self.request, gettext(
            f"Selamat room berhasil di edit."
        ))
        return redirect(f"/room/{room.slug}/")