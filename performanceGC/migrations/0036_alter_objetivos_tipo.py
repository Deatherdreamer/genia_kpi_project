# Generated by Django 4.1.7 on 2023-10-16 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0035_departamento_distribucion_alter_objetivos_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objetivos',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.distribucionobjetivo'),
        ),
    ]
