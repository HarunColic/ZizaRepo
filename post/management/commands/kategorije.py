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
            'Poljoprivredne',
            'Šumarske',
            'Ribolovne',
            'Rudarske',
            'Prerađivačke',
            'Energetske', #ENERGETSKE
            'Vodene i ekološke',#VODENE I EKOLOSKE
            'Građevinske',
            'Trgovačke' #TRGOVINA
            'Automehaničarske', #SERVIS VOZILA
            'Prijevozne i skladišne',
            'Ugostiteljske', # HORECA
            'IT', #IT
            'Finansijske', #FINANSIJSKE DJELATNOSTI
            'Osiguravajuće',  #OSIGURANJA
            'Poslovanje nekretninama', #NEKRETNINE
            'Stručne, '
            'Znanstvene'
            'Tehničke',
            'Administrativne i uslužne',
            'Javno upravne i odbrambene',
            'Obrazovne',
            'Kućanske',
            'Ostale uslužne',
            'Umjetničke',
            'Zabavne i rekreacijske',
            'Zdravstvene',
            ]
        categories2 = [

            'Administrativne i slične usluge',
            'Arhitektonske usluge',
            'Bankarstvo',
            'Biotehnologija i farmacija',
            'Državna služba i uprava',
            'Ekologija',
            'Ekonomija i finansije',
            'Elektrotehnika',
            'Mašinstvo',
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