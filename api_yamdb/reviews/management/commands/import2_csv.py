import os
import django
from django.core.management.base import BaseCommand
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User
import csv
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()


DATA = {
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'user.csv'
}

CSV_PATH = f'{settings.BASE_DIR}/static/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, csv_file in DATA.items():
            with open(
                str(CSV_PATH) + csv_file, 'r', newline=''
            ) as file:
                reader = csv.DictReader(file)
                records = []
                for row in reader:
                    records.append(model(**row))

            model.objects.bulk_create(records)
            self.stdout.write(
                self.style.SUCCESS('Successfully closed poll', model)
            )
