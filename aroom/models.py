from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
class Contact(models.Model):
    Id = models.AutoField
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=250)
    Address = models.CharField(max_length=550)
    Messages = models.TextField()
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Email

class User(AbstractUser):
    username = None
    # Id = models.AutoField
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, default="")
    address = models.TextField(default="")
    image = models.ImageField(upload_to ='pchat/images', null = True, blank = True)
    date = models.DateField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomUserManager()

    def __str__(self):
        return self.email


