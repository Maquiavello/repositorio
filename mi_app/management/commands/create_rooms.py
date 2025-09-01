import logging

from django.core.management.base import BaseCommand
from mi_app.models import Sala

# Configura el logger para que los mensajes aparezcan en la consola de Render
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Crea las salas de chat iniciales si no existen.'

    def handle(self, *args, **options):
        # Lista de nombres de salas que deseas crear
        room_names = ['Sala 1', 'Sala 2', 'Sala 3', 'Sala 4']
        
        # Itera sobre la lista y crea cada sala si no existe ya
        for room_name in room_names:
            try:
                # El método get_or_create es seguro para múltiples procesos y es atómico
                sala, created = Sala.objects.get_or_create(name=room_name)
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Sala "{sala.name}" creada exitosamente.'))
                else:
                    self.stdout.write(self.style.WARNING(f'La sala "{sala.name}" ya existe. Saltando.'))

            except Exception as e:
                # Si ocurre un error, lo registramos y continuamos
                self.stdout.write(self.style.ERROR(f'Error al crear la sala "{room_name}": {e}'))

