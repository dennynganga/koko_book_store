# Generated by Django 2.2.1 on 2019-05-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20190521_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='amount_charged',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
