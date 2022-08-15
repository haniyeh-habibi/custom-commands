from django.db import models


# Create your models here.
class Issues(models.Model):
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=300)
    is_open = models.BooleanField()


class Comments(models.Model):
    text = models.ForeignKey(Issues, on_delete=models.CASCADE, max_length=300)
    author = models.CharField(max_length=20)



