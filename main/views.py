from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cliente, Producto, Venta, DetalleVenta
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProductoForm
from .forms import ClienteForm # Asegúrate de tener un formulario ClienteForm creado
from .forms import UsuarioForm
from django.db import IntegrityError


# Create your views here.

# Página pública (productos sin posibilidad de compra)
def productos_publicos(request):
    productos = Producto.objects.all()
    return render(request, 'productos_publicos.html', {'productos': productos})

# Página de inicio
def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})

# Sirve para login requerido
@login_required
def registro_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                cliente_existente = Cliente.objects.filter(user=request.user).first()
                if cliente_existente:
                    return render(request, "registro_cliente.html", {"form": form, "error": "Ya tienes un cliente asociado."})
                cliente = form.save(commit=False)
                cliente.user = request.user
                cliente.save()
                return redirect("inicio")
            except IntegrityError:
                return render(request, "registro_cliente.html", {"form": form, "error": "Este cliente ya está registrado."})
    else:
        form = ClienteForm()
    return render(request, "registro_cliente.html", {"form": form})

# Registrar a los usuarios
def registrar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)  # Autenticar automáticamente después del registro
                return redirect("inicio")
            except IntegrityError:
                form.add_error("username", "El nombre de usuario ya está en uso.")
    else:
        form = UsuarioForm()
    return render(request, "registro.html", {"form": form})

# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('productos_publicos')

# Escritorio del administrador
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    detalles = DetalleVenta.objects.select_related('venta', 'producto').all()
    return render(request, 'admin_dashboard.html', {'detalles': detalles})

# Ver todos los productos
@user_passes_test(lambda u: u.is_superuser)
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ver_productos.html', {'productos': productos})

# Agregar un nuevo producto
@user_passes_test(lambda u: u.is_superuser)
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ver_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

# Editar un producto existente
@user_passes_test(lambda u: u.is_superuser)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('ver_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

# Eliminar un producto
@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

# Confirma las compras a realizar
@login_required
def confirmar_compra(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        cliente = request.user.cliente  # Intenta acceder al cliente del usuario autenticado
    except Cliente.DoesNotExist:
        # Redirige a una página de error si el cliente no existe
        return render(request, 'error_cliente.html', {
    'mensaje': 'No tiene un cliente asociado. Por favor, complete su perfil para realizar compras.'})
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > producto.existecias:
            return render(request, 'compra_error.html', {'producto': producto, 'error': 'existecias insuficiente.'})

        total = producto.precio * cantidad

        # Registrar la venta
        venta = Venta.objects.create(cliente=cliente, total=total)
        detalle = DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            subtotal=total
        )

        # Reducir el stock del producto
        producto.existecias -= cantidad
        producto.save()

        return render(request, 'compra_confirmada.html', {'detalle': detalle})

    return render(request, 'confirmar_compra.html', {'producto': producto})

# Ver todas las ventas realizadas
@login_required
def ver_ventas(request):
    if not request.user.is_superuser:
        return redirect('inicio')

    ventas = Venta.objects.prefetch_related('detalles').all()
    return render(request, 'ver_ventas.html', {'ventas': ventas})