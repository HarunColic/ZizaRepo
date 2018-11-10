from post.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        kategorije = Category.objects.filter(type=1)

        for k in kategorije:
            k.type = 4