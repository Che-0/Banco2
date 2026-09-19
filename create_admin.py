import os
import json
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_if_missing(user_data):
    username = user_data.get('username')
    password = user_data.get('password')

    if not username:
        print('Se omitió un usuario porque no tiene username.')
        return

    if not password:
        print(f"Se omitió el usuario '{username}' porque no tiene contraseña.")
        return

    email = user_data.get('email', '')
    telefono = user_data.get('telefono', '')
    rol = user_data.get('rol', User.Rol.CLIENTE)
    is_active = bool(user_data.get('is_active', True))
    is_superuser = bool(user_data.get('is_superuser', False))

    user = User.objects.filter(username=username).first()

    if user:
        # Actualiza contraseña y datos en cada deploy
        user.email = email
        user.telefono = telefono
        user.rol = rol
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.is_staff = is_superuser or user.is_staff
        user.set_password(password)
        user.save()
        print(f"Usuario '{username}' actualizado (contraseña incluida).")
        return

    if is_superuser:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            telefono=telefono,
            rol=rol,
        )
        print(f"Superusuario '{username}' creado exitosamente.")
    else:
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            telefono=telefono,
            rol=rol,
        )
        print(f"Usuario '{username}' creado exitosamente.")

seed_users = [
    {
        'username': os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
        'email': os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
        'password': os.environ.get('DJANGO_SUPERUSER_PASSWORD'),
        'telefono': os.environ.get('DJANGO_SUPERUSER_TELEFONO', ''),
        'rol': os.environ.get('DJANGO_SUPERUSER_ROL', User.Rol.ADMIN),
        'is_superuser': os.environ.get('DJANGO_SUPERUSER_IS_SUPERUSER', 'true').lower() == 'true',
        'is_active': os.environ.get('DJANGO_SUPERUSER_IS_ACTIVE', 'true').lower() == 'true',
    }
]

extra_users = os.environ.get('DJANGO_SEED_USERS', '')
if extra_users.strip():
    try:
        parsed_users = json.loads(extra_users)
    except json.JSONDecodeError as exc:
        print(f'No se pudo leer DJANGO_SEED_USERS: {exc}')
        sys.exit(1)

    if not isinstance(parsed_users, list):
        print('DJANGO_SEED_USERS debe ser una lista JSON de objetos de usuario.')
        sys.exit(1)

    seed_users.extend(parsed_users)

for user_data in seed_users:
    create_user_if_missing(user_data)