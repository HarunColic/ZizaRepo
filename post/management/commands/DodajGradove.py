from post.models import Category
from django.core.management.base import BaseCommand, CommandError
from location.models import City


class Command(BaseCommand):

    def handle(self, *args, **options):

        gradovi = [

            'Banja Luka',

            'Banovići',

            'Bihać',

            'Bijeljina',

            'Bosanska Krupa',

            'Brčko',

            'Bugojno',

            'Cazin',

            'Derventa',

            'Doboj',

            'Gradačac',

            'Gradiška',

            'Gračanica',

            'Jajce',

            'Kakanj',

            'Kalesija',

            'Konjic',

            'Kozarska Dubica',

            'Laktaši',

            'Livno',

            'Ljubuški',

            'Lukavac',

            'Maglaj',

            'Modriča',

            'Mostar',

            'Novi Grad',

            'Novi Travnik',

            'Prijedor',

            'Prnjavor',

            'Republika Srpska',

            'Republika Srpska',

            'Sanski Most',

            'Sarajevo',

            'Srebrenik',

            'Teslić',

            'Tešanj',

            'Tomislavgrad',

            'Travnik',

            'Trebinje',

            'Tuzla',

            'Velika Kladuša',

            'Visoko',

            'Vitez',

            'Zavidovići',

            'Zenica',

            'Zvornik',

            'Čapljina',

            'Široki Brijeg',

            'Žepče',

            'Živinice',

        ]

        for g in gradovi:

            if not City.objects.filter(name=g).exists():

                g = City(name=g)
                g.save()
