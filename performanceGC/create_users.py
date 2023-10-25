from django.contrib.auth.models import User
from .models import Empleado

empleados = Empleado.objects.all()

for empleado in empleados:
    # Create username from first word of nombre and first word of apellido
    nombre, apellido = empleado.nombre.split()[0], empleado.apellido.split()[0]
    username = f"{nombre.lower()}.{apellido.lower()}"
    
    # Create user with default password
    password = 'default_password'
    user = User.objects.create_user(username=username, password=password)
    
    # Associate user with empleado
    empleado.usuario = user
    empleado.save()