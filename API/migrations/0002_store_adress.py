# Generated by Django 3.2.19 on 2023-06-24 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='adress',
            field=models.CharField(blank=True, default='-', max_length=500),
        ),
    ]
