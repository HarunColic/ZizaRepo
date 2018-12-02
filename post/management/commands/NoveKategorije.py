from post.models import Category
from django.core.management.base import BaseCommand
import csv
import os


class Command(BaseCommand):

    def handle(self, *args, **options):

        kategorije = Category.objects.filter(type=1)

        for k in kategorije:
            k.type = 4
            k.save()

        folder = os.getcwd()

        with open(folder + '/file.csv') as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                i = 0
                cat = Category(name=row[i], type=1)
                i += 1
                cat.save()
