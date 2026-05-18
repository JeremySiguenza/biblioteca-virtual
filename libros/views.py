from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Libro, Prestamo

import random


# 🔔 NOTIFICACIONES
def obtener_notificaciones(usuario):

    if not usuario.is_authenticated:
        return []

    notificaciones = []

    prestamos = Prestamo.objects.filter(
        usuario=usuario,
        activo=True
    )

    # 📚 LIBROS PRESTADOS
    cantidad = prestamos.count()

    if cantidad > 0:

        notificaciones.append(
            f"📚 Tienes {cantidad} libros prestados"
        )

    # 🔥 FECHAS
    for prestamo in prestamos:

        dias_restantes = (
            prestamo.fecha_limite.date()
            - timezone.now().date()
        ).days

        # ⚠️ VENCIDO
        if dias_restantes < 0:

            notificaciones.append(
                f"⚠️ '{prestamo.libro.titulo}' está vencido"
            )

        # ⏳ PRÓXIMO A VENCER
        elif dias_restantes <= 2:

            notificaciones.append(
                f"⏳ '{prestamo.libro.titulo}' vence en {dias_restantes} días"
            )

        # ✅ RECIÉN PRESTADO
        elif dias_restantes >= 6:

            notificaciones.append(
                f"✅ Prestaste '{prestamo.libro.titulo}' correctamente"
            )

    return notificaciones

# 📚 LISTA DE LIBROS
def lista_libros(request):

    query = request.GET.get('q')

    if query:

        libros = Libro.objects.filter(
            titulo__icontains=query
        )

    else:

        libros = Libro.objects.all()

    return render(request, 'libros.html', {
        'libros': libros,
        'notificaciones': obtener_notificaciones(request.user)
    })


# ⭐ RECOMENDACIONES
def recomendaciones(request):

    usuario = request.user

    todos_libros = list(Libro.objects.all())

    # 🚫 SIN LIBROS
    if not todos_libros:

        return render(request, 'recomendaciones.html', {
            'recomendados': [],
            'mensaje': "No hay libros disponibles",
            'notificaciones': obtener_notificaciones(request.user)
        })

    # 🔥 USUARIO LOGGEADO
    if usuario.is_authenticated:

        prestamos = Prestamo.objects.filter(
            usuario=usuario,
            activo=True
        )

        categorias = [
            p.libro.categoria
            for p in prestamos
        ]

        # 🔥 LIBROS YA PRESTADOS
        libros_prestados = Prestamo.objects.filter(
            usuario=usuario,
            activo=True
        ).values_list(
            'libro_id',
            flat=True
        )

        # 🔥 RECOMENDADOS
        recomendados = Libro.objects.filter(
            categoria__in=categorias
        ).exclude(
            id__in=libros_prestados
        ).distinct()

        # 🚀 SI NO HAY RECOMENDADOS
        if not recomendados.exists():

            recomendados = random.sample(
                todos_libros,
                min(3, len(todos_libros))
            )

    # 👤 USUARIO NO LOGGEADO
    else:

        recomendados = random.sample(
            todos_libros,
            min(3, len(todos_libros))
        )

    # 🔥 MENSAJE
    if not usuario.is_authenticated:

        mensaje = "Explora nuestras recomendaciones"

    else:

        prestamos = Prestamo.objects.filter(
            usuario=usuario,
            activo=True
        )

        if not prestamos.exists():

            mensaje = "Recomendaciones destacadas para ti"

        else:

            mensaje = "Recomendaciones personalizadas para ti"

    return render(request, 'recomendaciones.html', {
        'recomendados': recomendados,
        'mensaje': mensaje,
        'notificaciones': obtener_notificaciones(request.user)
    })


# 📖 PRESTAR LIBRO
@login_required
def prestar_libro(request, libro_id):

    libro = Libro.objects.get(id=libro_id)

    # 🚫 EVITAR DUPLICADO
    if Prestamo.objects.filter(
        usuario=request.user,
        libro=libro,
        activo=True
    ).exists():

        messages.warning(
            request,
            "Ya tienes este libro prestado"
        )

        return redirect('inicio')

    # ✅ DISPONIBLE
    if libro.disponible:

        Prestamo.objects.create(
            usuario=request.user,
            libro=libro
        )

        libro.disponible = False
        libro.save()

        messages.success(
            request,
            "Libro prestado correctamente"
        )

    # ❌ NO DISPONIBLE
    else:

        messages.error(
            request,
            "Este libro no está disponible"
        )

    return redirect('inicio')


# 📚 MIS LIBROS
@login_required
def mis_libros(request):

    prestamos = Prestamo.objects.filter(
        usuario=request.user,
        activo=True
    )

    return render(request, 'mis_libros.html', {
        'prestamos': prestamos,
        'notificaciones': obtener_notificaciones(request.user)
    })


# 🔄 DEVOLVER LIBRO
@login_required
def devolver_libro(request, prestamo_id):

    prestamo = Prestamo.objects.get(
        id=prestamo_id
    )

    # 🔒 VALIDAR USUARIO
    if prestamo.usuario == request.user:

        libro = prestamo.libro

        libro.disponible = True
        libro.save()

        # 🔥 HISTORIAL
        prestamo.activo = False
        prestamo.fecha_devolucion = timezone.now()
        prestamo.save()

        messages.success(
            request,
            "Libro devuelto correctamente"
        )

    else:

        messages.error(
            request,
            "No puedes devolver este libro"
        )

    return redirect('mis_libros')


# 🔐 LOGIN
class CustomLoginView(LoginView):

    template_name = 'login.html'


# 🚪 LOGOUT
def logout_view(request):

    logout(request)

    return redirect('login')


# 📊 DASHBOARD
@login_required
def dashboard(request):

    total_libros = Libro.objects.count()

    total_prestamos = Prestamo.objects.filter(
        activo=True
    ).count()

    total_usuarios = Prestamo.objects.values(
        'usuario'
    ).distinct().count()

    return render(request, 'dashboard.html', {
        'total_libros': total_libros,
        'total_prestamos': total_prestamos,
        'total_usuarios': total_usuarios
    })


# 👤 REGISTRO
def registro(request):

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Usuario creado correctamente"
            )

            return redirect('login')

    else:

        form = UserCreationForm()

    return render(request, 'registro.html', {
        'form': form
    })

# 📜 HISTORIAL
@login_required
def historial(request):

    prestamos = Prestamo.objects.filter(
        usuario=request.user
    ).order_by('-fecha_solicitud')

    return render(request, 'historial.html', {
        'prestamos': prestamos,
        'notificaciones': obtener_notificaciones(request.user)
    })