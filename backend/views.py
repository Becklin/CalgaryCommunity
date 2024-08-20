from numpy import sort
import pandas as pd
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from .models import Community, CrimesReport, Service, Income
from decimal import Decimal
from .serializers import (
    CommunitySerializer,
    CrimesReportSerializer,
    ServiceSerializer,
    IncomeSerializer,
)
from django.db import connection
from .services import fetch_crimes_reports


# Create your views here.
class CommunityListView(generics.ListAPIView):
    # Avoid naming 'Community' class, which clash with Community.objects.all()
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    name = "community"


class CommunityDetailView(generics.RetrieveAPIView):
    # 在 Django REST framework (DRF) 中，使用 generics.RetrieveAPIView 创建视图时，不需要特别明确定义 comm_id，
    # 因为 DRF 已经为你处理了大部分通用情况。具体来说，RetrieveAPIView 使用了通用的 retrieve 动作，
    # 这个动作会根据请求中的 pk 参数（主键）自动检索相应的对象。

    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    name = "community-detail"


class CrimesReportListView(generics.ListAPIView):
    # queryset = CrimesReport.objects.all()
    # serializer_class = CrimesReportSerializer
    name = "crimes-report"

    def get(self, request, *args, **kwargs):
        records = fetch_crimes_reports()
        return JsonResponse({"data": records})


# get a community crimes report
class CrimesReportDetailView(generics.ListAPIView):
    serializer_class = CrimesReportSerializer
    name = "crimes-detail"

    def get_queryset(self):
        community = self.kwargs["community"]
        return CrimesReport.objects.filter(community=community)


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    name = "service"


class IncomeListView(generics.ListAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    name = "income"


def community_service_counts(request):
    results = Community.objects.services_within_5km()
    return JsonResponse(results)


class community_rank(generics.ListAPIView):
    name = "community_rank"

    def get(self, request, *args, **kwargs):
        # prepare data
        records = fetch_crimes_reports()
        community = list(Community.objects.all().values())
        community = sorted(community, key=lambda x: x.get("id"))
        services = Community.objects.services_within_5km()

        # remove the missing IDs from community and sevices
        ids_in_communities = {comm["id"] for comm in community}
        ids_in_records = {record["community_id"] for record in records}
        missing_ids = ids_in_communities - ids_in_records

        serviceList = list(services.items())
        for id in missing_ids:
            community[:] = [comm for comm in community if comm.get("id") != id]
            services.pop(id, None)
        sortedServices = sorted(services.items(), key=lambda x: x[0])

        # Normalize services
        min_service = min(sortedServices, key=lambda x: x[1])
        max_service = max(sortedServices, key=lambda x: x[1])
        services_normalized = [
            (y - min_service[1]) / (max_service[1] - min_service[1])
            for (x, y) in sortedServices
        ]
        sortedServices = [{x: y} for x, y in sortedServices]

        # Normalize incomes
        min_income = min(community, key=lambda x: x.get("income"))
        max_income = max(community, key=lambda x: x.get("income"))
        incomes_normalized = [
            (x.get("income") - min_income.get("income"))
            / (max_income.get("income") - min_income.get("income"))
            for x in community
        ]
        # Normalize crime records
        min_record = min(records, key=lambda x: x["total_whole_year"])
        max_record = max(records, key=lambda x: x["total_whole_year"])
        records_normalized = [
            (r["total_whole_year"] - min_record["total_whole_year"])
            / (max_record["total_whole_year"] - min_record["total_whole_year"])
            for r in records
        ]
        # Weights
        crime_weight = 0.4
        income_weight = 0.2
        service_weight = 0.4
        # Calculate desirability scores
        desirability_scores = [
            float(Decimal(c) * Decimal(crime_weight))
            + (i * income_weight)
            + float(r * Decimal(service_weight))
            for c, i, r in zip(
                services_normalized, incomes_normalized, records_normalized
            )
        ]

        # Step 1: 將 services_list 轉為 DataFrame
        service_df = pd.DataFrame(
            [(key, value) for d in sortedServices for key, value in d.items()],
            columns=["index", "service_count"],
        )

        # 設置 'index' 為 DataFrame 的索引
        service_df.set_index("index", inplace=True)

        # # Step 2: 將 info_list 轉為 DataFrame
        community_df = pd.DataFrame(community)

        # # Step 3: 將 scores_list 加入 info_df
        community_df["score"] = desirability_scores

        # Step 4: 合併 services_df 和 info_df
        final_df = pd.merge(community_df, service_df, left_on="id", right_index=True)

        # # Step 5: 選擇需要的列並改列名
        final_df = final_df[
            ["id", "income", "service_count", "name", "class_name", "score"]
        ]
        final_df.rename(columns={"class_name": "type"}, inplace=True)

        # # Step 6: 轉換成 list of dict
        result = final_df.to_dict(orient="records")

        # # 結果輸出
        return JsonResponse({"data": result})


# Create DataFrame
