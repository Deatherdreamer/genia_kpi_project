# Generated by Django 4.1.7 on 2023-06-21 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0018_valorescompetencias'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacioncompetencia',
            name='competencia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.competencias'),
        ),
    ]
