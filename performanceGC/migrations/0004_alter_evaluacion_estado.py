# Generated by Django 4.1.7 on 2023-04-25 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0003_remove_evaluacion_fechaentrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(0, 'Autoevaluacion'), (1, 'Evaluacion')], default=0, null=True),
        ),
    ]
