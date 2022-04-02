from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class RegisterAccount(UserCreationForm):
    """For create forms register

    Args:
        UserCreationForm (_type_): _description_
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", 
                  "email", "password1", "password2",]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["required"] = "true"
        self.fields["first_name"].widget.attrs["autofocus"] = "true"
        self.fields["last_name"].widget.attrs["required"] = "true"
        self.fields["email"].widget.attrs["required"] = "true"
        self.fields["username"].widget.attrs.pop("autofocus")