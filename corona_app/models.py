from django.db import models

class Noticias(models.Model):
    titular = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500)
    fuente = models.CharField(max_length=200)

# Create your models here.
