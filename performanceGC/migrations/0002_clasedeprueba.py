# Generated by Django 4.1.7 on 2023-04-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClasedePrueba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
            ],
        ),
    ]
