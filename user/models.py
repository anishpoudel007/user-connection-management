from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contact_number = models.CharField(max_length=50)
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    user_code = models.CharField(max_length=50)
