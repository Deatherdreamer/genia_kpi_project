# Generated by Django 4.1.7 on 2023-04-27 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0006_evaluacion_comr2_alter_evaluacion_comr1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='peso1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='peso2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='peso3',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='peso4',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]