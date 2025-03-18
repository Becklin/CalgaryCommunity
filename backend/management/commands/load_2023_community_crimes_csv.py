import pandas as pd
from django.core.management.base import BaseCommand
from backend.models import Community, CrimesReport


class Command(BaseCommand):
    help = "Load data from a CSV file into the database"

    def handle(self, *args, **kwargs):
        # name_to_id_map = {comm.name: comm.id for comm in Community.objects.all()}

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
        notexist = 0
        for index, row in data.iterrows():
            print(row["CommunityName"])
            # Fetch the Community instance
            try:
                communityInstance = Community.objects.get(name=row["CommunityName"])
            except Community.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Community {row["CommunityName"]} does not exist for row {index}'
                    )
                )
                notexist += 1
                continue  # Skip this iteration if the community does not exist
            crimes_report = CrimesReport(
                category=row["Category"],
                # name_to_id_map = {comm.name: comm.id for comm in Community.objects.all()}
                community=communityInstance,
                # name_to_id_map
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
            # print("crimes_report", crimes_report.community)
        print("notexist", notexist)
        self.stdout.write(self.style.SUCCESS("Successfully loaded geospatial data"))
