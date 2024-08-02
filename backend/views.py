from django.shortcuts import render
from rest_framework import generics
from .models import Community, CrimesReport
from .serializers import CommunitySerializer, CrimesReportSerializer


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
    queryset = CrimesReport.objects.all()
    serializer_class = CrimesReportSerializer
    name = "crimes-report"


# get a community crimes report
class CrimesReportDetailView(generics.ListAPIView):
    serializer_class = CrimesReportSerializer

    def get_queryset(self):
        community = self.kwargs["community"]
        return CrimesReport.objects.filter(community=community)

    name = "crimes-detail"
