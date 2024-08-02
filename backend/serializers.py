from .models import Community, CrimesReport
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class CrimesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimesReport
        fields = "__all__"
