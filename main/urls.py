from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', productos_publicos, name='productos_publicos'),
    path('inicio/', inicio, name='inicio'),
    path("registro/", registrar_usuario, name="registro"),
    path("registro_cliente/", registro_cliente, name="registro_cliente"),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('productos/', ver_productos, name='ver_productos'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('compra/<int:producto_id>/', confirmar_compra, name='confirmar_compra'),
    path('ventas/', ver_ventas, name='ver_ventas'),
]

