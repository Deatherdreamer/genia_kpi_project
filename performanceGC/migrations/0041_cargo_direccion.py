# Generated by Django 4.1.7 on 2023-10-18 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0040_alter_cargo_gerencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='direccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.direccion'),
        ),
    ]
