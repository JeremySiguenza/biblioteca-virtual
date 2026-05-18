from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# 🔥 FECHA LÍMITE AUTOMÁTICA
def fecha_limite_default():
    return timezone.now() + timedelta(days=7)


# 📚 LIBROS
class Libro(models.Model):

    titulo = models.CharField(
        max_length=100
    )

    autor = models.CharField(
        max_length=100
    )

    categoria = models.CharField(
        max_length=50
    )

    disponible = models.BooleanField(
        default=True
    )

    # 🌐 Imagen por URL
    imagen = models.URLField(
        blank=True
    )

    def __str__(self):

        return self.titulo


# 🔄 PRÉSTAMOS
class Prestamo(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE
    )

    # 📅 Fecha solicitud
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True
    )

    # 📅 Fecha límite devolución
    fecha_limite = models.DateTimeField(
        default=fecha_limite_default
    )

    # 📅 Fecha devolución real
    fecha_devolucion = models.DateTimeField(
        null=True,
        blank=True
    )

    # ✅ Activo o devuelto
    activo = models.BooleanField(
        default=True
    )

    # ⚠️ VALIDAR SI ESTÁ VENCIDO
    def vencido(self):

        return (
            timezone.now() > self.fecha_limite
            and self.activo
        )

    def __str__(self):

        return f"{self.usuario} - {self.libro}"