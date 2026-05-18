from django.contrib import admin
from .models import Libro, Prestamo


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):

    list_display = (
        'titulo',
        'autor',
        'categoria',
        'disponible'
    )

    search_fields = (
        'titulo',
        'autor'
    )

    list_filter = (
        'categoria',
        'disponible'
    )


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):

    list_display = (
        'usuario',
        'libro',
        'fecha_solicitud',
        'activo'
    )

    list_filter = (
        'activo',
    )