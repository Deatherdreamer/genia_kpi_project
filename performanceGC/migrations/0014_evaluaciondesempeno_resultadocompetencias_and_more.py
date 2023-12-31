# Generated by Django 4.1.7 on 2023-06-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0013_rename_peso_objetivoactividad_pesoactividad'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluaciondesempeno',
            name='resultadoCompetencias',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='evaluaciondesempeno',
            name='resultadoFinal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='evaluaciondesempeno',
            name='resultadoObjetivos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
