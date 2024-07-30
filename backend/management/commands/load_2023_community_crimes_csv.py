import pandas as pd
from django.core.management.base import BaseCommand
from backend.models import CrimesReport


class Command(BaseCommand):
    help = "Load data from a CSV file into the database"

    def handle(self, *args, **kwargs):

        data = pd.read_csv("2023_Community_Crime_and_Disorder_Statistics.csv")
        data = data.dropna(how="all")
        data[
            [
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC",
            ]
        ] = data[
            [
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC",
            ]
        ].fillna(
            0
        )
        for index, row in data.iterrows():
            crimes_report = CrimesReport(
                category=row["Category"],
                community_name=row["CommunityName"],
                january=row["JAN"],
                february=row["FEB"],
                march=row["MAR"],
                april=row["APR"],
                may=row["MAY"],
                june=row["JUN"],
                july=row["JUL"],
                august=row["AUG"],
                september=row["SEP"],
                october=row["OCT"],
                november=row["NOV"],
                december=row["DEC"],
            )
            crimes_report.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data"))
