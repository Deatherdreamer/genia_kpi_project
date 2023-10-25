# Generated by Django 4.1.7 on 2023-08-16 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0032_actividades_created_actividades_createdby_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(default='')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora', models.TimeField(auto_now_add=True)),
                ('de', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to='performanceGC.empleado')),
                ('para', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to='performanceGC.empleado')),
            ],
        ),
    ]
