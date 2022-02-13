from django import forms
from .models import CustomUser,FileUpload

from django.contrib.auth import get_user_model


class User(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('email','password')

class UpdateUser(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('email','name','username','phone','is_active')


class FileUploadForm(forms.ModelForm):
    class Meta:
        model=FileUpload
        fields=['file_upload']
