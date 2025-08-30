from django.db import models

# Create your models here.

class usuarios(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)

    def __str__(self):
        return self.usuario + ' - ' + self.correo

class Sala(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    users = models.ManyToManyField(usuarios, related_name='salas_joined', blank=True)

    def __str__(self):
        return self.name
