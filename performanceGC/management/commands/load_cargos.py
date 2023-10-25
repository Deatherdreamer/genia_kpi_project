import pandas as pd
from django.core.management.base import BaseCommand
from performanceGC.models import Cargo

class Command(BaseCommand):
    help = 'Loads cargo data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The path to the Excel file')

    def handle(self, *args, **options):
        filename = options['filename']
        df = pd.read_excel(filename)
        cargos = []
        for index, row in df.iterrows():
            cargo = Cargo(nombre=row['Nombre'], descripcion=row['Descripcion'], salario=row['Salario'])
            cargos.append(cargo)
        Cargo.objects.bulk_create(cargos)
        self.stdout.write(self.style.SUCCESS('Successfully loaded cargo data from Excel file.'))