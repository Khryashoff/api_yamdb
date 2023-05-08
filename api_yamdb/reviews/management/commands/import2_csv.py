import os
import django
from django.core.management.base import BaseCommand
from reviews.models import Category
# from users.models import User
import csv
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()


DATA = {
    # Genre: 'genre.csv',
    Category: 'category.csv',
    # Title: 'title.csv',
    # Review: 'review.csv',
    # Comment: 'comments.csv',
    # User: 'user.csv'
}

CSV_PATH = f'{settings.BASE_DIR}/static/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, csv_file in DATA.items():
            with open(
                str(CSV_PATH) + csv_file, 'r') as file:
                reader = csv.DictReader(file)
                records = []
                line_counter = 0
                for row in reader:
                    if line_counter == 0:
                        line_counter += 1
                        continue
                    line_counter += 1
                    records.append(model(**row))

            model.objects.bulk_create(records)
            self.stdout.write(self.style.SUCCESS('Successfully closed poll', model))