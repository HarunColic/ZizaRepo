from post.models import Category
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):

        kategorije = Category.objects.all()

        for k in kategorije:

            if k.name == "Administrativne i slične usluge" or k.name == "Arhitektonske usluge" or k.name == "Bankarstvo" \
                    or k.name == "Menadžment i upravljanje" or k.name == "Nauka - Istraživački rad" or k.name == "Obrazovanje" \
                    or k.name == "Pravo" or k.name == "Veterina" or k.name == "Zdravstvo":
                k.slika = 1
            elif k.name == "Državna služba i uprava" or k.name == "Osiguranje" or k.name == "Policija - Zaštitarske usluge" or k.name == "Turizam":
                k.slika = 2
            elif k.name == "Ekonomija i finansije" or k.name == "Računovodstvo - Revizija":
                k.slika = 3
            elif k.name == "Građevinarstvo":
                k.slika = 4
            elif k.name == "Ljepota i zdravlje":
                k.slika = 5
            elif k.name == "Ekologija":
                k.slika = 6
            elif k.name == "Biotehnologija i farmacija" or k.name == "Mašinstvo" or k.name == "Energetika" or k.name == "Mali oglasi"\
                    or k.name == "Oglasi ZZZRS" or k.name == "Ostalo" or k.name == "Rudarstvo" or k.name == "Ugostiteljstvo"\
                    or k.name == "Umjetnost i dizajn":
                k.slika = 7
            elif k.name == "Elektrotehnika" or k.name == "Grafička industrija" or k.name == "Grafički dizajn" or k.name == "Informatika - Hardware" \
                    or k.name == "Informatika - Software" or k.name == "IT" or k.name == "Telekomunikacije":
                k.slika = 8
            elif k.name == "Transport - Skladištenje i logistika" or k.name == "Zabava" or k.name == "Zanatske usluge"\
                    or k.name == "Poljoprivreda - Ribarstvo - Šumarstvo" or k.name == "Prehrambena Industrija" or k.name == "Proizvodnja"\
                    or k.name == "Saobraćaj i komunikacije" or k.name == "Socijalne usluge - Neprofitne organizacije":
                k.slika = 9
            elif k.name == "Marketing - PR" or k.name == "Mediji":
                k.slika = 10
            elif k.name == "Komercijala - Prodaja" or k.name == "Konsalting" or k.name == "Nekretnine":
                k.slika = 12

        for k in kategorije:
            k.save()