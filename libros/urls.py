from django.urls import path
from . import views


urlpatterns = [

    # 📚 INICIO
    path(
        '',
        views.lista_libros,
        name='inicio'
    ),

    # ⭐ RECOMENDACIONES
    path(
        'recomendaciones/',
        views.recomendaciones,
        name='recomendaciones'
    ),

    # 📚 MIS LIBROS
    path(
        'mis-libros/',
        views.mis_libros,
        name='mis_libros'
    ),

    # 📖 PRESTAR
    path(
        'prestar/<int:libro_id>/',
        views.prestar_libro,
        name='prestar'
    ),

    # 🔄 DEVOLVER
    path(
        'devolver/<int:prestamo_id>/',
        views.devolver_libro,
        name='devolver'
    ),

    # 🔐 LOGIN
    path(
        'login/',
        views.CustomLoginView.as_view(),
        name='login'
    ),

    # 🚪 LOGOUT
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # 👤 REGISTRO
    path(
        'registro/',
        views.registro,
        name='registro'
    ),

    # 📊 DASHBOARD
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
    'historial/',
    views.historial,
    name='historial'
    ),

]