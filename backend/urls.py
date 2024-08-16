from django.urls import path
from . import views
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(
        "community/",
        views.CommunityListView.as_view(),
        name=views.CommunityListView.name,
    ),
    path(
        "communityDetail/<str:pk>",
        views.CommunityDetailView.as_view(),
        name=views.CommunityDetailView.name,
    ),
    path(
        "crimesReport/",
        views.CrimesReportListView.as_view(),
        name=views.CrimesReportListView.name,
    ),
    path(
        "crimesReport/<str:community>",
        views.CrimesReportDetailView.as_view(),
        name=views.CrimesReportDetailView.name,
    ),
    path(
        "service/",
        views.ServiceListView.as_view(),
        name=views.ServiceListView.name,
    ),
    path(
        "income/",
        views.IncomeListView.as_view(),
        name=views.IncomeListView.name,
    ),
    path(
        "community-service-counts/",
        views.community_service_counts,
        name="community_service_counts",
    ),
]
# enable us to get json data
urlpatterns = format_suffix_patterns(urlpatterns)
