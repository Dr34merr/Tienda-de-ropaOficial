#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import os
from django.contrib.auth.models import User


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TiendaOficial.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

def create_superuser():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "Administrador")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "allmoshecasia@gmail")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "12345@adm")
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superusuario '{username}' creado exitosamente.")
    else:
        print(f"Superusuario '{username}' ya existe.")

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    if os.getenv("CREATE_SUPERUSER", "False") == "True":
        import django
        django.setup()
        create_superuser()
    execute_from_command_line()
