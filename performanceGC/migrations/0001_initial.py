# Generated by Django 4.1.7 on 2023-04-25 18:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreText', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('nombre', models.TextField(max_length=200)),
                ('apellido', models.TextField(max_length=200)),
                ('cedula', models.IntegerField(default=0)),
                ('ficha', models.IntegerField(default=0)),
                ('ceco', models.CharField(max_length=15)),
                ('fechaIngreso', models.DateField(blank=True, null=True, verbose_name='Fecha de Ingreso')),
                ('fechaEgreso', models.DateField(blank=True, null=True)),
                ('fechaNacimiento', models.DateField(blank=True, null=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performanceGC.cargo')),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Niveles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField(choices=[(0, 'VIP'), (1, 'GERENTE DE PRIMERA LINEA'), (2, 'GERENTE DE SEGUNDA LINEA'), (3, 'JEFE'), (4, 'COORDINADOR'), (5, 'ASESOR DE NEGOCIOS'), (6, 'ESPECIALISTA'), (7, 'ANALISTA'), (8, 'TECNICO O INSPECTOR'), (9, 'ASESOR DE FARMACIA'), (10, 'ASISTENTE'), (11, 'OPERARIO'), (12, 'AUXILIAR')])),
                ('porCompetencias', models.IntegerField(default=50)),
                ('cantidadCompetencias', models.IntegerField(default=2)),
                ('cantidadObjetivos', models.IntegerField(default=4)),
                ('porObjetivos', models.IntegerField(default=50)),
                ('nivel', models.TextField(choices=[('BASE', 'BASE'), ('COORDINACION O JEFATURA', 'COORDINACION O JEFATURA'), ('GERENCIA', 'GERENCIA'), ('DIRECCION', 'DIRECCION'), ('ESPECIALISTA O SUPERVISOR', 'ESPECIALISTA O SUPERVISOR')])),
            ],
        ),
        migrations.CreateModel(
            name='Gerencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreText', models.CharField(max_length=200)),
                ('direccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='performanceGC.direccion')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fechaentrega', models.DateTimeField()),
                ('estado', models.IntegerField(choices=[(0, 'Autoevaluacion'), (1, 'Evaluacion')], default=0)),
                ('obj1', models.TextField(default='')),
                ('peso1', models.IntegerField(default=5)),
                ('valor1', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('resultado1', models.IntegerField(default=0)),
                ('observaciones1', models.TextField(default='')),
                ('obj2', models.TextField(default='')),
                ('peso2', models.IntegerField(default=5)),
                ('valor2', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('resultado2', models.IntegerField(default=0)),
                ('observaciones2', models.TextField(default='')),
                ('obj3', models.TextField(default='')),
                ('peso3', models.IntegerField(default=5)),
                ('valor3', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('resultado3', models.IntegerField(default=0)),
                ('observaciones3', models.TextField(default='')),
                ('obj4', models.TextField(blank=True, null=True)),
                ('peso4', models.IntegerField(blank=True, default=5, null=True)),
                ('valor4', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('resultado4', models.IntegerField(blank=True, default=0, null=True)),
                ('observaciones4', models.TextField(blank=True, null=True)),
                ('com1', models.TextField(default='')),
                ('comv1', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('comr1', models.IntegerField(blank=True, default=0, null=True)),
                ('com2', models.TextField(default='')),
                ('comv2', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('com3', models.TextField(blank=True, null=True)),
                ('comv3', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('comr3', models.IntegerField(blank=True, default=0, null=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performanceGC.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='DetallesEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performanceGC.evaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='Competencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('nivel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performanceGC.niveles')),
            ],
        ),
        migrations.AddField(
            model_name='cargo',
            name='gerencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performanceGC.gerencia'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='nivel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.niveles'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='performanceGC.cargo'),
        ),
    ]