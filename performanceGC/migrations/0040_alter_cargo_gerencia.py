# Generated by Django 4.1.7 on 2023-10-18 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0039_direccion_debajo_gerencia_debajo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='gerencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.gerencia'),
        ),
    ]
