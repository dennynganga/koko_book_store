# Generated by Django 2.2.1 on 2019-05-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_book_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
