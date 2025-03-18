from numpy import sort
import pandas as pd
import json
from django.contrib.gis.geos import MultiPolygon, Point
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from .models import fetch_crimes_reports, Community, CrimesReport, Service, Income
from decimal import Decimal
from .serializers import (
    CommunitySerializer,
    CrimesReportSerializer,
    ServiceSerializer,
    IncomeSerializer,
    RankingSerializer,
)

from .services import RankingService


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


class community_rank(generics.CreateAPIView):
    name = "community_rank"

    def post(self, request, *args, **kwargs):
        serializer = RankingSerializer(data=request.data)

        if serializer.is_valid():
            crimesWeights = serializer.validated_data["crimes"]
            servicesWeights = serializer.validated_data["services"]
            incomeWeights = serializer.validated_data["income"]

        ranking_service = RankingService(crimesWeights, servicesWeights, incomeWeights)
        community_with_scores = ranking_service.calculate_scores()
        print("格", community_with_scores[0])
        return JsonResponse({"data": community_with_scores})
