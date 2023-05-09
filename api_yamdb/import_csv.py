from reviews.models import Genre, Category, Title, Review
import csv
file_path = 'static/data/genre.csv'

with open('static/data/genre.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        genres = Genre(id=id, name=name, slug=slug)
        genres.save()
    csv_file.close()


with open('static/data/category.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        category = Category(id=id, name=name, slug=slug)
        category.save()
    csv_file.close()


with open('static/data/titles.csv', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        id = row['id']
        name = row['name']
        year = row['year']
        # не указываю категорию - ошибка
        title = Title(id=id, name=name, year=year)
        title.save()
    csv_file.close()

with open('static/data/review.csv', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        id = row['id']
        title_id = row['title_id']
        text = row['text']
        author_id = row['author']
        score = row['score']
        pub_date = row['pub_date']
        review = Review(
            id=id,
            title_id=title_id,
            author_id=author_id,
            score=score,
            pub_date=pub_date)
        review.save()
    csv_file.close()
