from django.views import View
import requests
import json
from django.contrib.gis.geos import MultiPolygon, Point
from rest_framework import generics
from django.http import JsonResponse
from .models import fetch_crimes_reports, Community, CrimesReport, Service, Income
from decimal import Decimal
from .serializers import (
    CommunityBasicSerializer,
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
        results = {}
        for key, url in self.API_URLS.items():
            results[key] = self.fetch_data_from_api(url)
        return JsonResponse({"data": results})

    def fetch_data_from_api(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


# Create your views here.
class CommunityListView(generics.ListAPIView):
    queryset = Community.objects.only("id", "name", "multipolygon", "class_name")
    serializer_class = CommunityBasicSerializer
    name = "community"


class CommunityDetailView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    name = "community-detail"


class CrimesReportListView(generics.ListAPIView):
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
