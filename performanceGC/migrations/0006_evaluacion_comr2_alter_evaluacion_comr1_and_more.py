# Generated by Django 4.1.7 on 2023-04-27 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0005_evaluacion_comentarios_evaluacion_ncom1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='comr2',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='comr1',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='comr3',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='resultado1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='resultado2',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='resultado3',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='resultado4',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='totalCom',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='totalObj',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
