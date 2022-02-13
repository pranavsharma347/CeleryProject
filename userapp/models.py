from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser,PermissionsMixin):

    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username = models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=6,unique=True)
    phone=models.CharField(max_length=14,null=True,blank=True)
    is_active= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects=CustomUserManager()


class FileUpload(models.Model):
    file_upload=models.FileField(upload_to='documents')
