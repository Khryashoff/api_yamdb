import pandas as pd
import os
import django
# import csv
from reviews.models import Genre


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

csv_file_path = 'static/data/titles.csv'

data = pd.read_csv(csv_file_path)

for index, row in data.iterrows():
    new_entry = Genre(
        id=row['id'],
        name=row['name'],
        slug=row['slug'],
        # category=row['category_id']
    )
    new_entry.save()
print('Import Complete!')

# with open('static/data/titles.csv') as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)  # skip header row
#     records = []

#     for row in reader:
#         records.append(Title(**row))
#     Title.objects.bulk_create(records)
#     print("Успешно!")