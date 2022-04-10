from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User") # User model

class RoomNotFoundError(ValidationError):
    pass

class UserNotFoundError(ValidationError):
    pass

class UserExistInRoom(ValidationError):
    pass

class CategoriesBase(models.Model):
    """Model to implementation category of classroom

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    title = models.CharField(_("title"), max_length=30, help_text=_("Masukkan nama kelas yang akan di sediakan."))
    slug = models.SlugField()
    desc = models.TextField(_("deskripsi"), max_length=255)
    is_active = models.BooleanField(_("aktif"), default=False)
    mentor = models.ManyToManyField(AUTH_USER_MODEL, blank=False, related_name="user_mentor_in_rooms")
    created = models.DateTimeField(_("dibuat"), auto_now_add=True)
    
    class Meta:
        abstract = True

class RoomManager(models.Manager):
    """Model manager

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    def get_room_from_pk(self, room_pk):
        """Mendapatkan room dari filtering pk
        
        Args:
            room_pk (str): primary key dari room
        """
        try:
            room = Room.objects.get(pk=room_pk)
        except Room.DoesNotExist:
            raise RoomNotFoundError(_("Mohon maaf room tidak ditemukan."))
        return room
    
    def get_user_from_username(self, username):
        """Mendapatkan user filtering username          

        Args:
            username (str): username dari pengguna
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise UserNotFoundError(_("Mohon maad user tidak ditemukan."))
        return user
        
    def join_room(self, room_pk, username) -> bool:
        """Fungsi untuk membuat pengguna bisa bergabung ke dalam room

        Args:
            room_pk (int): id dari room
            username (str): username pengguna

        Returns:
            _type_: _description_
        """
        room = self.get_room_from_pk(room_pk)
        user = self.get_user_from_username(username)
        if not user in room.member.all():
            room.member.add(user)
            room.save()
            return True
        else:
            return False
    
    def quit_room(self, room_pk, username) -> bool:
        """Fungsi untuk membuat pengguna bisa keluar dari room

        Args:
            room_pk (int): primary key dari room
            username (str): username dari pengunaq

        Returns:
            bool: True: Jika berhasil, False: Jika gagal atau tidak ada username di dalam room
        """
        room = self.get_room_from_pk(room_pk)
        user = self.get_user_from_username(username)
        if user in room.member.all():
            room.member.remove(user)
            room.save()
            return True
        else:
            return False
    
    def get_all_mentor(self, room_pk) -> list:
        """Fungsi untuk mengembalikan semua data mentor dari room

        Args:
            room_pk (_type_): room pk

        Returns:
            list: List data dari mentor room
        """
        room = self.get_room_from_pk(room_pk)
        mentor = room.mentor.all()
        return mentor
    
    def get_all_member(self, room_pk) -> list:
        """Fungsi untuk mengembalikan semua data member dari room

        Args:
            room_pk (_type_): room pk

        Returns:
            list: List data dari member room
        """
        room = self.get_room_from_pk(room_pk)
        member = room.member.all()
        return member
        

class Room(CategoriesBase):
    """Model to implementation room of classroom

    Args:
        models (_type_): _description_
    """
    logo = models.ImageField(_("logo"), upload_to="logo")
    member = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name="user_member_in_rooms")
    content = RichTextUploadingField(verbose_name=_("konten"), blank=True)
    tags = TaggableManager(blank=True)
    opened = models.TimeField(_("jam buka"), blank=False, null=False)
    closed = models.TimeField(_("jam tutup"), blank=False, null=False)
    
    def __str__(self) -> str:
        return self.title
    
    objects = RoomManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class AuthenticatedJoinQuitRoom(models.Model):
    """Model untuk autentikasi gabung room

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    to_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="join_to_rooms")
    from_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="join_from_users")
    choices = models.CharField(_("pilihan"), max_length=4, choices=[("join", _("Gabung")),
                                                                    ("quit", _("Keluar"))])
    message = models.CharField(_("pesan"), max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(_("%s ingin bergabung ke room %s" % (self.from_user, self.to_room)))
    
    def save(self, *args, **kwargs):
        if self.choices == "quit":
            self.message = "%s ingin keluar dari room %s" % (self.from_user, self.to_room)
        if self.choices == "join":
            self.message = "%s ingin bergabung ke room %s" % (self.from_user, self.to_room)
        super(AuthenticatedJoinQuitRoom, self).save(*args, **kwargs)