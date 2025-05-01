from django.views import View
from numpy import sort
import pandas as pd
import requests
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

class FetchAndProcessDataView(View):
    API_URLS = {
        "boundaries": "https://data.calgary.ca/resource/surr-xmvs.json",
        "services": "https://data.calgary.ca/resource/x34e-bcjz.json",
        "income": "https://data.calgary.ca/resource/wj3a-wgmh.json",
    }

    def get(self, request):
        result = self.fetch_data_from_api(self.API_URLS['boundaries'])
        print(result)
        return JsonResponse({"data": result})
        # try:
        #     # 執行資料擷取與處理
        #     self.process_boundaries(self.fetch_data_from_api(self.API_URLS['boundaries']))
        #     self.process_services(self.fetch_data_from_api(self.API_URLS['services']))
        #     self.process_income(self.fetch_data_from_api(self.API_URLS['income']))

        #     return JsonResponse({"status": "success", "message": "資料已更新並儲存至資料庫"})
        # except Exception as e:
        #     return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # Step 1: 抓取 API 資料
    def fetch_data_from_api(self, url):
        response = requests.get(url)
        response.raise_for_status()
        result= response.json()
        print(result)
        return result

    # # Step 2: 處理社區邊界資料
    # def process_boundaries(self, data):
    #     CommunityBoundary.objects.all().delete()  # 清除舊資料
    #     for item in data:
    #         try:
    #             name = item.get('name', 'Unknown')
    #             area = float(item.get('area', 0))
    #             geometry_data = item.get('the_geom', None)
                
    #             # 使用 GEOSGeometry 處理 GeoJSON
    #             geom = GEOSGeometry(json.dumps(geometry_data)) if geometry_data else None

    #             CommunityBoundary.objects.create(name=name, area=area, geom=geom)
    #         except Exception as e:
    #             print(f"處理社區邊界資料失敗: {e}")

    # # Step 3: 處理社區服務資料
    # def process_services(self, data):
    #     CommunityService.objects.all().delete()  # 清除舊資料
    #     for item in data:
    #         try:
    #             name = item.get('name', 'Unknown')
    #             address = item.get('address', 'Unknown Address')
    #             service_type = item.get('type', 'Unknown Type')
    #             latitude = float(item.get('latitude', 0))
    #             longitude = float(item.get('longitude', 0))
                
    #             geom = Point(longitude, latitude, srid=4326)

    #             CommunityService.objects.create(
    #                 name=name,
    #                 address=address,
    #                 type=service_type,
    #                 geom=geom
    #             )
    #         except Exception as e:
    #             print(f"處理社區服務資料失敗: {e}")

    # # Step 4: 處理收入資料
    # def process_income(self, data):
    #     CommunityIncome.objects.all().delete()  # 清除舊資料
    #     for item in data:
    #         try:
    #             community_name = item.get('community_name', 'Unknown')
    #             median_income = float(item.get('median_income', 0))
    #             average_income = float(item.get('average_income', 0))

    #             CommunityIncome.objects.create(
    #                 community_name=community_name,
    #                 median_income=median_income,
    #                 average_income=average_income
    #             )
    #         except Exception as e:
    #             print(f"處理收入資料失敗: {e}")

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
        return JsonResponse({"data": community_with_scores})
