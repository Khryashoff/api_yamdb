import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User
from reviews.models import Genre, Category, Title, Review, Comment


DATA = {
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'users.csv'
}

CSV_PATH = f'{settings.BASE_DIR}/static/data/'


class Command(BaseCommand):
    """
    Загружает данные csv в базу данных.
    """
    def handle(self, *args, **options):
        for model, csv_file in DATA.items():
            with open(
                str(CSV_PATH) + csv_file, 'r', newline='', encoding='utf-8'
            ) as file:
                reader = csv.DictReader(file)
                records = []
                for row in reader:
                    records.append(model(**row))

            model.objects.bulk_create(records)
            self.stdout.write(
                self.style.SUCCESS('Данные csv успешно внесены.')
            )
