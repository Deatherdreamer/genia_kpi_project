# Generated by Django 4.1.7 on 2023-06-08 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0012_objetivoactividad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objetivoactividad',
            old_name='peso',
            new_name='pesoActividad',
        ),
    ]