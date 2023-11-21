# Generated by Django 4.1.7 on 2023-10-18 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0038_alter_periodo_año_fin_alter_periodo_año_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='direccion',
            name='debajo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.direccion'),
        ),
        migrations.AddField(
            model_name='gerencia',
            name='debajo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.gerencia'),
        ),
    ]