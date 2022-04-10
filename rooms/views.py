from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.translation import gettext
from django.views import generic
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpRequest
from django.db.models import Q 
from functools import reduce
import operator

from rooms.forms import RoomEditForm

from rooms.models import Room, AuthenticatedJoinQuitRoom

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
        else:
            request_joined_or_quited = AuthenticatedJoinQuitRoom.objects.all() # Permintaan bergabung
            is_waiting = ""
            is_mentor = False
            for rjq in request_joined_or_quited:
                if self.request.user == rjq.from_user and self.object == rjq.to_room:
                    if rjq.choices == "join":
                        is_waiting = gettext("Menunggu Konfirmasi Gabung")
                    else:
                        is_waiting = gettext("Menunggu Konfirmasi keluar")
                else:
                    is_waiting = False
                if self.request.user in rjq.to_room.mentor.all():
                    is_mentor = True
                else:
                    is_mentor = False
            return render(request, self.template_name, {self.context_object_name: self.get_queryset(),
                                                        "is_index_active": self.is_index_active,
                                                        "request_joined_or_quited": request_joined_or_quited,
                                                        "is_mentor": is_mentor,
                                                        "is_waiting": is_waiting})

class RoomDetailView(generic.DetailView, LoginRequiredMixin):
    """Halaman detail tentang kelas

    Args:
        generic (_type_): _description_
    """
    template_name = "rooms/room.html"
    model = Room
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_joined_or_quited = AuthenticatedJoinQuitRoom.objects.all() # Permintaan bergabung
        is_waiting = ""
        is_mentor = False
        for rjq in request_joined_or_quited:
            if self.request.user == rjq.from_user and self.object == rjq.to_room:
                if rjq.choices == "join":
                    is_waiting = gettext("Menunggu Konfirmasi Gabung")
                else:
                    is_waiting = gettext("Menunggu Konfirmasi keluar")
            else:
                is_waiting = False
            if self.request.user in rjq.to_room.mentor.all():
                is_mentor = True
            else:
                is_mentor = False
        context["request_joined_or_quited"] = request_joined_or_quited
        context["is_waiting"] = is_waiting
        context["is_mentor"] = is_mentor
        context["rooms"] = Room.objects.all()
        context["is_room_active"] = True # Active Web
        return context

def join_room(request, room_pk, username):
    """Fungsi untuk membuat pengguna bergabung ke dalam kelas tetapi harus melalui persetujuan dari admin terlebih dahulu.

    Args:
        request (_type_): _description_
        pk (_type_): _description_
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not request.user.is_authenticated:
        return redirect("account:login")
    else:
        room = get_object_or_404(Room, pk=room_pk)
        user = get_object_or_404(User, username=username)
        if user in room.member.all():
            # Jika pengguna telah bergabung ke dalam grub kelas
            messages.error(request, gettext(
                f"Mohon maaf anda sudah bergabung ke dalam kelas ini."
            ))
        else:
            # room.member.add(user)
            # room.save()
            auth = AuthenticatedJoinQuitRoom.objects.create(to_room=room, from_user=user, choices="join")
            messages.success(request, gettext(
                f"Terima kasih, permintaan anda menunggu konfirmasi dari mentor room ini."
            ))
        return redirect(f"/room/{room.slug}/#content")

def join_room_accepted(request, room_pk, username):
    """Setelah di konfirmasi oleh mentor maka pengguna bisa bergabung ke dalam room

    Args:
        request (_type_): _description_
        pk (_type_): room.pk
        username (_type_): username
    """
    if not request.user.is_authenticated:
        return redirect("account:login")
    else:
        user = get_object_or_404(User, username=username)
        room = get_object_or_404(Room, pk=room_pk)
        joined = Room.objects.join_room(room_pk, username)
        if joined:
            auth = AuthenticatedJoinQuitRoom.objects.get(to_room=room, from_user=user, choices="join")
            auth.delete()
            messages.success(request, gettext("Akun dengan nama pengguna %s di ijinkan bergabung ke dalam room %s" % (user.username, room)))
            return redirect(f"/room/{room.slug}/#content")

def join_room_rejected(request, room_pk, username):
    """Jika mentor tidak mengijinkan pengguna untuk bergabung ke dalam room

    Args:
        request (_type_): _description_
        room_pk (_type_): _description_
        username (_type_): _description_
    """
    if not request.user.is_authenticated:
        return redirect("account:login")
    else:
        room = get_object_or_404(Room, pk=room_pk)
        user = get_object_or_404(User, username=username)
        auth = get_object_or_404(AuthenticatedJoinQuitRoom, to_room=room, from_user=user)
        if auth:
            auth.delete()
            messages.warning(request, gettext(f"{user} tidak di ijinkan masuk kedalam room {room}."))
            return redirect(f"/room/{room.slug}/#content")
        else:
            messages.error(request, gettext(f"Ada sesuatu yang salah."))
            return redirect(f"/room/{room.slug}/#content")

def quit_room(request, room_pk, username):
    """Fungsi untuk membuat pengguna keluar dari kelas

    Args:
        request (_type_): _description_
        pk (_type_): _description_
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not request.user.is_authenticated:
        return redirect("account:login")
    else:
        user = get_object_or_404(User, username=username)
        room = get_object_or_404(Room, pk=room_pk)
        if user in room.member.all():
            # Jika pengguna telah bergabung ke dalam grub kelas
            # Maka bisa dikeluarkan.
            auth = AuthenticatedJoinQuitRoom.objects.create(to_room=room, from_user=user, choices="quit")
            messages.success(request, gettext(
                f"Terimakasih, permintaain keluar sedang di konfirmasi dari mentor room ini."
            ))
        else:
            messages.error(request, gettext(
                f"Mohon maaf, anda belum bergabung. Bagaimana bisa dikeluarkan hahahaha"
            ))
        return redirect(f"/room/{room.slug}/#content")
    
def quit_room_accepted(request, room_pk, username):
    """Setelah di konfirmasi oleh mentor maka pengguna akan keluar dari room

    Args:
        request (_type_): _description_
        pk (_type_): room.pk
        username (_type_): username
    """
    if not request.user.is_authenticated:
        return redirect("account:login")
    else:
        room = get_object_or_404(Room, pk=room_pk)
        user = get_object_or_404(User, username=username)
        quited = Room.objects.quit_room(room_pk, username)
        if quited:
            auth = AuthenticatedJoinQuitRoom.objects.get(to_room=room, from_user=user, choices="quit")
            auth.delete()
            messages.success(request, gettext("Akun dengan nama pengguna %s di ijinkan keluar dari room %s" % (user, room)))
            return redirect(f"/room/{room.slug}/#content")

def quit_room_rejected(request, room_pk, username):
    """Jika mentor tidak mengijinkan pengguna untuk keluar room

    Args:
        request (_type_): _description_
        room_pk (_type_): _description_
        username (_type_): _description_
    """
    if not request.user.is_authenticated:
        return redirect("account:login")
    else:
        room = get_object_or_404(Room, pk=room_pk)
        user = get_object_or_404(User, username=username)
        auth = get_object_or_404(AuthenticatedJoinQuitRoom, to_room=room, from_user=user)
        if auth:
            auth.delete()
            messages.warning(request, gettext(f"{user} tidak di ijinkan keluar room {room}."))
            return redirect(f"/room/{room.slug}/#content")
        else:
            messages.error(request, gettext(f"Ada sesuatu yang salah."))
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
    
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs.get("pk"))
        if request.user not in room.mentor.all():
            # Jika user yang masuk bukanlah mentor maka akan ditolak
            messages.warning(request, gettext("Maaf anda tidak berhak mengedit room ini, karena anda bukanlah mentor dari room ini."))
            return redirect(f"/room/{room.slug}/#content")
        else:
            # Jika user adalah mentor maka permintaan akan diterima
            return render(request, self.template_name, {"form": self.form_class(instance=room), "room": room})
    
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