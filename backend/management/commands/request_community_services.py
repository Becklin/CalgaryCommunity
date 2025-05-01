import requests
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, Point
from backend.models import Service


class Command(BaseCommand):
    help = "Load community services from the API into the database"

    def handle(self, *args, **kwargs):
        api_url = "https://data.calgary.ca/resource/x34e-bcjz.json"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Failed to fetch data from the API"))
            return
        
        data = response.json()  # Parse the JSON data
        for index, row in enumerate(data):
            if "POINT" in row and row["POINT"]:
                point_coords = row["POINT"].split(",")  # Assuming POINT is in "lat,lon" format
                lat = float(point_coords[0])
                lon = float(point_coords[1])
                service_geo_data = Service(
                    type=row.get("TYPE", ""),
                    name=row.get("NAME", ""),
                    address=row.get("ADDRESS", ""),
                    comm_code=row.get("COMM_CODE", ""),
                    point=Point(lon, lat),
                )
                service_geo_data.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data from API"))

