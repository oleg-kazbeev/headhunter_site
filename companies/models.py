from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from headhunter_site.settings import MEDIA_COMPANY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
