from .models import Community, CrimesReport, Service, Income
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class CrimesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimesReport
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"


class RankingSerializer(serializers.Serializer):
    crimes = serializers.IntegerField()
    services = serializers.IntegerField()
    income = serializers.IntegerField()
