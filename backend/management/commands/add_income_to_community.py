from django.core.management.base import BaseCommand
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.db.models.functions import Centroid
from backend.models import Income, Community


class Command(BaseCommand):
    help = "add household income from Income to Community"

    def handle(self, *args, **kwargs):
        # 初始化每個 Community 的 total_income 為 0
        Community.objects.update(income=0)

        # 遍歷所有的 Community
        for community in Community.objects.all():
            total_income = 0

            # 遍歷所有的 Income
            for income in Income.objects.all():
                # 檢查 Community 是否完全位於 Income 的多邊形內
                if income.polygon.intersects(community.multipolygon):
                    total_income = income.total_household_total_income
            # 更新 Community 的 total_income
            community.income = total_income
            community.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully aggregated total household income to communities"
            )
        )
