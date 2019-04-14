from django.core.management.base import BaseCommand
from location.models import Region


class Command(BaseCommand):

    def handle(self, *args, **options):

        kantoni = ['Sarajevo', 'Unsko-sanski', 'Posavski', 'Tuzlanski', 'Zeničko-dobojski', 'Bosansko-podrinjski',
                   'Srednjobosanski', 'Hercegovačko-neretvanski', 'Zapadno-hercegovački', 'Livanjski', 'Banjalučka',
                   'Dobojsko-Bijeljinska', 'Sarajevsko-Zvornička', 'Trebinjsko-Fočanska', 'Distrikt Brčko']

        for k in kantoni:

            r = Region(name=k)
            r.save()
