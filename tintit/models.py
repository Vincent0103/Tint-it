from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Wallpapers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    desc = models.TextField(max_length=160, blank=True)
    file_img = models.ImageField(blank=True, upload_to='wallpapers')
    url_img = models.URLField(blank=True)
    allow_comments = models.BooleanField()
    likes = models.IntegerField(auto_created=True, default=0)
    upload_date = models.DateTimeField(auto_now_add=True)