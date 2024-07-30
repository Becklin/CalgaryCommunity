import csv
import pandas as pd
import geojson
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from backend.models import Community
from datetime import datetime


class Command(BaseCommand):
    help = "Load geospatial data from a CSV file into the database"

    def handle(self, *args, **kwargs):
        csv_file_path = "Community_District_Boundaries_20240727.csv"
        data = pd.read_csv(csv_file_path)

        for index, row in data.iterrows():
            multipolygon = GEOSGeometry(row["MULTIPOLYGON"])

            community_geo_data = Community(
                class_code=row["CLASS_CODE"],
                comm_code=row["COMM_CODE"],
                name=row["NAME"],
                sector=row["SECTOR"],
                srg=row["SRG"],
                comm_structure=row["COMM_STRUCTURE"],
                created_dt=datetime.strptime(row["CREATED_DT"], "%Y/%m/%d"),
                modified_dt=datetime.strptime(row["MODIFIED_DT"], "%Y/%m/%d"),
                multipolygon=multipolygon,
            )
            print("geo_data", community_geo_data.multipolygon)
            community_geo_data.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data"))
