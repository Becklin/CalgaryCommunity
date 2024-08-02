# update_fk.py

from django.core.management.base import BaseCommand
import pandas as pd
from backend.models import Community, CrimesReport


class Command(BaseCommand):
    help = (
        "Update CommunityName field in CrimesReport based on the id field in Community"
    )

    def handle(self, *args, **kwargs):

        name_to_id_map = {comm.name: comm.id for comm in Community.objects.all()}

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

        print("name_to_id_map", name_to_id_map)

        for report in CrimesReport.objects.all():
            print(report)
            # new_community_name_value = name_to_id_map.get(report.community_name)
            # if new_community_name_value:
            #     report.community_name = new_community_name_value
            #     # report.save()
            #     self.stdout.write(
            #         self.style.SUCCESS(
            #             f"Successfully updated Community id {Community.pk}"
            #         )
            #     )
            # else:
            #     self.stdout.write(
            #         self.style.WARNING(
            #             f"No matching value for Model2 id {Community.pk}"
            #         )
            #     )
