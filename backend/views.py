from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from .models import Community, CrimesReport, Service, Income
from .serializers import (
    CommunitySerializer,
    CrimesReportSerializer,
    ServiceSerializer,
    IncomeSerializer,
)
from django.db import connection


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
        records = self.run_custom_sql()
        return JsonResponse({"data": records})

    def run_custom_sql(self):
        sql = """
        SELECT community_id, 
               SUM(whole_year) AS total_whole_year
        FROM (
            SELECT community_id, 
                   category, 
                   SUM(january + february + march + april + may + june + july + august + september + october + november + december) AS whole_year
            FROM backend_crimesreport
            GROUP BY community_id, category
        ) AS subquery
        GROUP BY community_id
        ORDER BY community_id;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

            # 构建结果列表
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in results]


# get a community crimes report
class CrimesReportDetailView(generics.ListAPIView):
    serializer_class = CrimesReportSerializer

    def get_queryset(self):
        community = self.kwargs["community"]
        return CrimesReport.objects.filter(community=community)

    name = "crimes-detail"


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
