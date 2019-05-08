from post.models import Category
from django.core.management.base import BaseCommand, CommandError
from location.models import City, Region


class Command(BaseCommand):

    def handle(self, *args, **options):

        gradovi = City.objects.all()
        Sarajveo = ["Hadžići","Ilidža","Ilijaš","Sarajevo - Centar","Sarajevo-Novi Grad","Sarajevo-Novo Sarajevo","Sarajevo-Stari Grad","Trnovo","Vogošća", "Sarajevo"]

        sa = Region.objects.get(name='Sarajevo')

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Bihać","Bosanska Krupa","Bosanski Petrovac","Bužim","Cazin","Ključ","Sanski Most","Velika Kladuša"]

        sa = Region.objects.get(name="Unsko-sanski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Domaljevac","Odžak","Orašje", "Šamac"]

        sa = Region.objects.get(name="Posavski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Banovići","Doboj-Istok","Gradačac","Gračanica","Kalesija","Kladanj","Lukavac","Sapna","Srebrenik","Teočak","Tuzla","Čelić","Živinice"]

        sa = Region.objects.get(name="Tuzlanski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Breza","Doboj-Jug","Kakanj","Maglaj","Olovo","Tešanj","Usora","Vareš","Visoko","Zavidovići","Zenica","Žepče"]

        sa = Region.objects.get(name="Zeničko-dobojski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Foča","Goražde","Pale"]

        sa = Region.objects.get(name="Bosansko-podrinjski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Bugojno","Busovača","Dobretići","Donji Vakuf","Fojnica","Gornji Vakuf - Uskoplje","Jajce","Kiseljak","Kreševo","Novi Travnik","Travnik","Vitez"]

        sa = Region.objects.get(name="Srednjobosanski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Mostar","Jablanica","Konjic","Neum","Prozor","Ravno","Stolac","Čapljina","Čitluk"]

        sa = Region.objects.get(name="Hercegovačko-neretvanski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Grude","Ljubuški","Posušje","Široki Brijeg"]

        sa = Region.objects.get(name="Zapadno-hercegovački")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Bosansko Grahovo","Drvar","Glamoč","Kupres","Livno","Tomislavgrad"]

        sa = Region.objects.get(name="Livanjski")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Banja Luka","Gradiška","Istočni Drvar","Jezero","Kneževo","Kostajnica","Kotor Varoš","Kozarska Dubica","Krupa na uni","Kupres","Laktaši","Mrkonjić Grad","Novi Grad","Oštra Luka","Petrovac","Prijedor","Prnjavor","Ribnik","Srbac","Čelinac","Šipovo"]

        sa = Region.objects.get(name="Banjalučka")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Bijeljina","Bosanski Brod","Derventa","Doboj","Donji Žabar","Lopare","Modriča","Pelagićevo","Petrovo","Stanari","Teslić","Ugljevik","Vukosavlje","Šamac"]

        sa = Region.objects.get(name="Dobojsko-Bijeljinska")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Berkovići","Bileća","Gacko","Istočni Mostar","Kalinovik","Ljubinje","Nevesinje","Trebinje","Čajniče"]

        sa = Region.objects.get(name="Trebinjsko-Fočanska")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Brčko"]

        sa = Region.objects.get(name="Distrikt Brčko")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        Sarajveo = ["Zvornik","Bratunac","Han Pijesak","Ilijaš","Istočni Stari Grad","Kasindo","Lukavica","Milići",
                    "Osmaci","Pale","Rogatica","Rudo","Sokolac","Srebrenica","Trnovo","Ustiprača","Višegrad","Vlasenica","Šekovići","Žepa"],

        sa = Region.objects.get(name="Sarajevsko-Zvornička")

        for g in gradovi:
            for s in Sarajveo:

                if g.name == s:
                    g.regionID = sa
                    g.save()

        zvornik = City.objects.get(name='Zvornik')
        zvornik.regionID = sa
        zvornik.save()
