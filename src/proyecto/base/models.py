from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                db_index=True)
    titulo = models.CharField(max_length=200,db_index=True)
    descripcion = models.TextField(null=True,
                                   blank=True)
    completo = models.BooleanField(default=False,db_index=True)
    creado = models.DateTimeField(auto_now_add=True,db_index=True)

    # Relación con Categoría (Una tarea pertenece a UNA categoría)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    # Relación con Etiquetas (Una tarea puede tener MUCHAS etiquetas)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['completo']