import csv
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, Point
from backend.models import Service


class Command(BaseCommand):
    help = "Load community services from a CSV file into the database"

    def handle(self, *args, **kwargs):
        csv_file_path = "Community_Services_20240806.csv"
        data = pd.read_csv(csv_file_path)
        for index, row in data.iterrows():

            original_point = GEOSGeometry(row["POINT"])
            print(original_point)
            service_geo_data = Service(
                type=row["TYPE"],
                name=row["NAME"],
                address=row["ADDRESS"],
                comm_code=row["COMM_CODE"],
                point=Point(original_point.y, original_point.x),
            )
            service_geo_data.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data"))
