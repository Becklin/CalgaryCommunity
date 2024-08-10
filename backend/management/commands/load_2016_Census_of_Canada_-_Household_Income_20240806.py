import csv
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from backend.models import Income


class Command(BaseCommand):
    help = "Load community incomes from a CSV file into the database"

    def handle(self, *args, **kwargs):
        csv_file_path = "2016_Census_of_Canada_-_Household_Income_20240806.csv"
        data = pd.read_csv(csv_file_path)
        for index, row in data.iterrows():
            print(row)
            polygon = GEOSGeometry(row["polygon"])

            service_geo_data = Income(
                ward=row["Ward"],
                total_household_total_income=row[
                    "Total - Household total income groups in 2015 for private households - 25% sample data"
                ],
                under_20_000=row["Under $20,000"],
                _20_000_to_39_999=row["$20,000 to $39,999"],
                _40_000_to_59_999=row["$40,000 to $59,999"],
                _60_000_to_79_999=row["$60,000 to $79,999"],
                _80_000_to_99_999=row["$80,000 to $99,999"],
                _100_000_to_124_999=row["$100,000 to $124,999"],
                _125_000_to_149_999=row["$125,000 to $149,999"],
                _150_000_to_199_999=row["$150,000 to $199,999"],
                _200_000_and_over=row["$200,000 and over"],
                polygon=polygon,
            )
            service_geo_data.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data"))
