# Generated by Django 4.1.7 on 2023-07-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0025_alter_empleado_cedula_alter_empleado_ficha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluaciondesempeno',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(0, 'Borrador'), (1, 'Autoevaluacion'), (2, 'Evaluacion')], default=0, null=True),
        ),
    ]
