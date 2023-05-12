# Project API YaMDb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

## Description
The YaMDb project collects user "Reviews" of works. Unfortunately, the works themselves are not stored in YaMDb, you can't watch a movie or listen to music here, but you can read about them.
The works are divided into categories such as "Books", "Movies", "Music".
A work can be assigned a "Genre" from the preset list.
Only the administrator can add works, categories and genres.
You can come to us and leave an assessment on the work you like, write an enthusiastic review for it, or vice versa, share your indignation at the next film from the Star Wars© saga. On the basis of the obtained estimates, an average estimate of the work is formed - a rating.
Users can leave "Comments" to reviews.
Only authenticated users can add reviews, comments and ratings, so please register.

## Technologies
- Python 3.9.10
- Django 3.2.16
- Django REST framework 3.12.4
- JWT + Djoser

## Launching a project in dev mode
1. Clone the repository and go to it on the command line:
```bash
git clone https://github.com/Khryashoff/api_yamdb.git
```
```bash
cd api_yamdb/
```
2. Install and activate the virtual environment for the project:
```bash
python -m venv venv
```
```bash
# for OS Windows
. venv/Scripts/activate
```
3. Update pip and install dependencies from the file requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
4. Perform migrations at the project level:
```bash
python manage.py migrate
```
5. Create a superuser:
```bash
python manage.py createsuperuser
```
6. Start the project:
```bash
python manage.py runserver
```

## User registration algorithm
1. The user sends a POST request to add a new user.
```
POST /api/v1/auth/signup/
```

Pass user data to body:
```json
{
"email": "string",
"username": "string"
}
```
2. YaMDB sends an email with a confirmation code (confirmation_code) to the email address.
3. The user sends a POST request to receive a JWT token. 
```
POST /api/v1/auth/token/
```

Pass user data to body:
```json
{
"username": "string",
"confirmation_code": "string"
}
```

Specify the received token in the Authorization field to access the full functionality of the project:
```
Authorization: Bearer Token {your_token}
```

4. If desired, the user sends a PATCH request to fill in the information in his profile (the description of the fields is in the documentation).
```
PATCH /api/v1/users/me/
```

## Request examples
```
GET, POST /api/v1/titles/ - receiving and creation works.
GET, PATCH, DEL /api/v1/titles/{titles_id}/  - receiving, editing and deletion of works.

GET, POST /api/v1/categories/ - getting and creating categories of works.
DEL /api/v1/categories/{slug}/ - deleting categories of works.

GET, POST /api/v1/genres/ - getting and creating genres of works.
DEL /api/v1/genres/{slug}/ - deleting genres of works.

GET, POST /api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/ - receiving and creating reviews for works.
GET, PATCH, DEL /api/v1/titles/{titles_id}/reviews/{reviews_id}/  - receiving, editing and deleting reviews of works.

GET, POST POST /api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/ - receiving and creating comments to reviews.
GET, PATCH, DEL /api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/{comment_id}/  - receiving, editing and deleting comments to reviews.
```

## Resources
```bash
# Project documentation
http://127.0.0.1:8000/redoc/
```

## Participants
Victoria Sergeeva [(vika6107)](https://github.com/vika6107) - user management (Auth and Users): registration and authentication system, access rights, token operation, e-mail confirmation system, fields;
Sergey Khryashchev [(Khryashoff)](https://github.com/Khryashoff) - Teamlead. Categories (Categories), genres (Genres) and works (Titles): models, views and endpoints for them;
Timur Gimadiev [(Timur)](https://github.com/Timur-Gimadiev)- reviews (Review) and comments (Comments): models and views, endpoints, access rights for requests. Ratings of works.
