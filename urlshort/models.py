from django.db import models

# Create your models here.


class UrlData(models.Model):
    original_url = models.URLField(max_length=1000)
    shortened_url = models.URLField(unique=True);
