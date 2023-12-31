# Generated by Django 4.1.7 on 2023-07-31 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceGC', '0027_alter_evaluacionobjetivo_comentarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='competencias',
            name='significado1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competencias',
            name='significado2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competencias',
            name='significado3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competencias',
            name='significado4',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competencias',
            name='valor1',
            field=models.IntegerField(blank=True, default=1, editable=False),
        ),
        migrations.AddField(
            model_name='competencias',
            name='valor2',
            field=models.IntegerField(blank=True, default=2, editable=False),
        ),
        migrations.AddField(
            model_name='competencias',
            name='valor3',
            field=models.IntegerField(blank=True, default=3, editable=False),
        ),
        migrations.AddField(
            model_name='competencias',
            name='valor4',
            field=models.IntegerField(blank=True, default=4, editable=False),
        ),
        migrations.DeleteModel(
            name='ValoresCompetencias',
        ),
    ]
