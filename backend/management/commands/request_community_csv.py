import requests
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon, LinearRing
from backend.models import Community
from datetime import datetime


class Command(BaseCommand):
    help = "Load geospatial data from the API into the database"

    def handle(self, *args, **kwargs):
        api_url = "https://data.calgary.ca/resource/surr-xmvs.json"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Failed to fetch data from the API"))
            return
        
        data = response.json()  # Parse the JSON data
        for index, row in enumerate(data):
            original_multipolygon = GEOSGeometry(row["MULTIPOLYGON"])
            multipolygon = self.swap_lat_lon_in_multipolygon(original_multipolygon)
            community_geo_data = Community(
                id=index,
                class_name=self.to_pascal_case(row["CLASS"]),
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
            community_geo_data.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data from API"))

    def swap_lat_lon_in_multipolygon(self, multipolygon):
        new_polygons = []
        for polygon in multipolygon:
            new_rings = []
            for ring in polygon:
                new_coords = [(y, x) for x, y in ring.coords]
                new_rings.append(LinearRing(new_coords))
            new_polygons.append(Polygon(*new_rings))
        return MultiPolygon(new_polygons)

    def to_pascal_case(self, s):
        return "".join(word.capitalize() for word in s.split())
