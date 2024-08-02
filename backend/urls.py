from django.urls import path
from . import views
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(
        "communities/",
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
]
# enable us to get json data
urlpatterns = format_suffix_patterns(urlpatterns)
