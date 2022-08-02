import email
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=120)
    email = models.EmailField()
    profile_pix = models.ImageField(upload_to="profiles/", blank=True, null=True)
    social_handle = models.CharField(max_length=100)
    
    def __str__(self):
        return self.fullname
    