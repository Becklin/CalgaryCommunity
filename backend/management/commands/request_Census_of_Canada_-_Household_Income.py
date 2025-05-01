import requests
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon, LinearRing
from backend.models import Income


class Command(BaseCommand):
    help = "Load community incomes from the API into the database"

    def handle(self, *args, **kwargs):
        api_url = "https://data.calgary.ca/resource/wj3a-wgmh.json"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Failed to fetch data from the API"))
            return
        
        data = response.json()  # Parse the JSON data
        for index, row in enumerate(data):
            if "polygon" in row and row["polygon"]:
                try:
                    original_polygon = GEOSGeometry(row["polygon"])
                    polygon = self.swap_lat_lon_in_multipolygon(original_polygon)

                    income_geo_data = Income(
                        ward=row.get("Ward", ""),
                        total_household_total_income=row.get(
                            "Total - Household total income groups in 2015 for private households - 25% sample data", 
                            0
                        ),
                        under_20_000=row.get("Under $20,000", 0),
                        _20_000_to_39_999=row.get("$20,000 to $39,999", 0),
                        _40_000_to_59_999=row.get("$40,000 to $59,999", 0),
                        _60_000_to_79_999=row.get("$60,000 to $79,999", 0),
                        _80_000_to_99_999=row.get("$80,000 to $99,999", 0),
                        _100_000_to_124_999=row.get("$100,000 to $124,999", 0),
                        _125_000_to_149_999=row.get("$125,000 to $149,999", 0),
                        _150_000_to_199_999=row.get("$150,000 to $199,999", 0),
                        _200_000_and_over=row.get("$200,000 and over", 0),
                        polygon=polygon,
                    )
                    income_geo_data.save()

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {index}: {e}"))
                    continue

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