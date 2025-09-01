# mi_app/management/commands/create_rooms.py
from django.core.management.base import BaseCommand
from mi_app.models import Sala

class Command(BaseCommand):
    help = 'Creates initial chat rooms for the application if they do not exist'

    def handle(self, *args, **options):
        room_names = ['Lobby', 'Lobby 2']
        for name in room_names:
            if not Sala.objects.filter(name=name).exists():
                Sala.objects.create(name=name)
                self.stdout.write(self.style.SUCCESS(f'Successfully created room: "{name}"'))
            else:
                self.stdout.write(f'Room "{name}" already exists. Skipping.')