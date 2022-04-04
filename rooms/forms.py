from turtle import title
from django import forms 
from rooms.models import Room
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms.widgets import TextInput, HiddenInput
from django.utils.translation import gettext

class RoomEditForm(forms.ModelForm):
    title = forms.CharField(max_length=150, widget=TextInput(), 
                            help_text=gettext("Masukkan title dari room yang akan digunakan."))
    class Meta:
        model = Room
        fields = ["title", "desc", "logo", "content",
                  "tags", "opened", "closed",]
    
    def __init__(self, *args, **kwargs):
        super(RoomEditForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["desc"].widget.attrs["class"] = "form-control"
        self.fields["logo"].widget.attrs["class"] = "form-control"
        # self.fields["member"].widget.attrs["class"] = "form-control"
        self.fields["content"].widget.attrs["class"] = "form-control"
        self.fields["opened"].widget.attrs["class"] = "form-control"
        self.fields["closed"].widget.attrs["class"] = "form-control"
        