from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User") # User model

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)