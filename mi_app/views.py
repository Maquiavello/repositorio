from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import usuarios, Sala
from django.contrib.auth.decorators import login_required
# Create your views here.

def registro(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        correo = request.POST['correo']
        
        contraseña_plana = request.POST['contraseña']
        if usuarios.objects.filter(usuario=usuario).exists():
            return render(request, 'registro.html',{
                'error': 'Este usuario ya está registrado'
            })
        if usuarios.objects.filter(correo=correo).exists():
            return render(request, 'registro.html', {
                'error': 'Este correo ya existe'
            })
        contraseña_encriptada = make_password(contraseña_plana)

        nuevo_usuario= usuarios(usuario=usuario, correo=correo, contraseña=contraseña_encriptada)
        nuevo_usuario.save()
        print("Usuario registrado exitosamente")
        print(f"Usuario: {usuario}")
        print(f"Correo: {correo}")
        print(f"Contraseña encriptada: {contraseña_encriptada}")
        return redirect ('login')
    else:
        return render(request, 'registro.html') 

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        contraseña = request.POST.get('contraseña', '').strip()

        if not usuario or not contraseña:
            return render(request, 'login.html', {
                'error': 'Por favor, completa todos los campos',
                'usuario_valor': usuario
            })

        try:
            user = usuarios.objects.get(usuario=usuario)

            print(f"Usuario encontrado: {user.usuario}")
            print(f"Contraseña en BD: {user.contraseña}")
            print(f"Contraseña ingresada: {contraseña}")
            if check_password(contraseña, user.contraseña):
                request.session['usuario_id'] = user.id
                # ✅ LOGIN EXITOSO
                print ("✅ Contraseña correcta!")
                return redirect ('menu')
            else:
                print("❌ Contraseña INCORRECTA")
                return render (request, 'login.html', {
                    'error': 'Contraseña incorrecta'
                })
        except usuarios.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Usuario no encontrado'
            })
    return render (request, 'login.html')

def logout(request):
    try:
        del request.session['usuario_id']
        print("Sesión cerrada correctamente.")
    except KeyError:
        pass
    return redirect('login')

def menu(request):
    Salas = Sala.objects.all()
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
            return redirect ('login')
    usuario_actual = usuarios.objects.get(id=usuario_id)
    return render (request, 'chat/menu.html', {
        'salas': Salas,
        'usuario': usuario_actual
    })


def sala(request, sala_id):
    try:
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect ('login')
        usuario_actual = usuarios.objects.get(id=usuario_id)
        sala = Sala.objects.get(id=sala_id)
        return render(request, 'chat/sala.html', {'sala': sala,
                                                   'usuario': usuario_actual})
    except Sala.DoesNotExist:
        return render(request, 'chat/sala.html', {'salas': sala,
                                                   'error': 'Esta sala no funciona'})