from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile, User
from post.models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from post.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        categories = [
            'Poljoprivreda, šumarstvo, ribolov',
            'Vađenje ruda i kamena',
            'Prerađivačka industrija',
            'Proizvodnja i opskrba električnom energijom, plinom, parom i klimatizacija',
            'Opskrba vodom; uklanjanje otpadnih voda, gospodarenje otpadom te djelatnosti sanacije okoliša',
            'Građevinarstvo',
            'Trgovina na veliko i na malo; popravak motornih vozila i motocikala',
            'Prijevoz i skladištenje',
            'Djelatnosti pružanja smještaja te pripreme i usluživanja hrane (hoteljerstvo i ugostiteljstvo)',
            'Informacije i komunikacije',
            'Financijske djelatnosti',
            'Djelatnosti osiguranja',
            'Poslovanje nekretninama',
            'Stručne, znanstvene i tehničke djelatnosti',
            'Administrativne i pomodne uslužne djelatnosti',
            'Javna uprava i obrana; obvezno socijalno osiguranje',
            'Obrazovanje',
            'Djelatnosti izvanteritorijalnih organizacija i tijela',
            'Djelatnosti kudanstava kao poslodavaca; djelatnosti kudanstava koja proizvode različita dobra i obavljaju različite usluge za vlastite potrebe',
            'Ostale uslužne djelatnosti',
            'Umjetnost, zabava i rekreacija',
            'Djelatnosti zdravstvene zaštite i socijalne skrbi',
            ]
        categories2 = [

            'Administrativne i slične usluge',
            'Arhitektonske usluge',
            'Bankarstvo',
            'Biotehnologija i farmacija',
            'Državna služba i uprava',
            'Ekologija',
            'Ekonomija i finansije',
            'Elektrotehnika - Mašinstvo',
            'Energetika',
            'Grafička industrija',
            'Grafički dizajn',
        ]

        for c in categories:
            cat = Category(name=c, type=0)
            cat.save()

        for c in categories2:
            cat = Category(name=c, type=1)
            cat.save()