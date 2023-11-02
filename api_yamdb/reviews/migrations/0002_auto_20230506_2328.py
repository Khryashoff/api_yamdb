# Generated by Django 3.2 on 2023-05-06 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('author', 'title')},
        ),
    ]