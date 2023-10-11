from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('user.User', models.CASCADE)