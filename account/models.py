from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _ 

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

def get_image_path(instance, filename):
    pass

class Account(models.Model):
    """Model to implementation account

    Args:
        models (_type_): _description_
    """
    # GENDER CHOICES 
    MALE = "MALE"
    FEMALE = "FEMALE"
    GENDER_CHOICES = (
        (FEMALE, _("Perempuan")),
        (MALE, _("Laki-laki")),
    )
    
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="user_accounts")
    bio = models.TextField(_("bio"), max_length=150, blank=True, null=True)
    photo_profile = models.ImageField(_("foto profile"), default="default-profile-img.png",
                                      upload_to=get_image_path)
    nim = models.IntegerField(_("nomor induk mahasiswa"), default=211)
    gender = models.CharField(_("jenis kelamin"), max_length=6,
                              choices=GENDER_CHOICES)
    
    # Enter room class name
    
    def __str__(self) -> str:
        return self.user.username

