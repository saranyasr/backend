from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class userModel(AbstractUser):
    email = models.CharField(max_length=50,null=False,blank=False,unique=True)
    
    REQUIRED_FIELDS = ['email']
   
    def __str__(self):
        return self.username