import datetime

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        invoice = datetime.datetime.strptime('24052010', "%d%m%Y").date()

        file_path = '%(year)04d/%(month)02d/%(day)02d/%(id)d.pdf' % {'year': invoice.year,
                                                           'month': invoice.month,
                                                           'day': invoice.day,
                                                           'id': 1}

        self.stdout.write(file_path)