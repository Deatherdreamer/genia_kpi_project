# Generated by Django 4.1.7 on 2023-06-21 17:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0021_alter_evaluacioncompetencia_pesocompetencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacioncompetencia',
            name='pesoCompetencia',
            field=models.PositiveIntegerField(default=0, help_text='Ingrese un valor entre 1 y 4.', validators=[django.core.validators.MaxValueValidator(4)]),
        ),
    ]