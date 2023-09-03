from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    full_name = models.CharField(max_length=100,null=True, blank=True )
    phone = models.CharField(max_length=20, null=True, blank=True)
    expired_date = models.DateTimeField(max_length=150,null=True, blank=True)
    def __str__(self) -> str:
        return super().__str__()