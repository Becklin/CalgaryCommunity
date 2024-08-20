from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.measure import D


# Create your models here.
class CommunityQuerySet(models.QuerySet):
    def services_within_distance(self):
        results = {}
        for community in self:
            center = community.multipolygon.centroid
            services_within_distance = Service.objects.filter(
                point__distance_lte=(center, D(km=5))
            ).exclude(type="Community Centre")
            Service_count = services_within_distance.count()
            results[community.id] = Service_count

        sorted_communities = dict(
            sorted(results.items(), key=lambda x: x[1], reverse=True)
        )
        return sorted_communities


class CommunityManager(models.Manager):
    def get_queryset(self):
        return CommunityQuerySet(self.model, using=self._db)

    def services_within_5km(self):
        return self.get_queryset().services_within_distance()


class Community(models.Model):
    class_name = models.CharField(max_length=50, null=True, blank=True)
    class_code = models.CharField(max_length=50)
    comm_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255, unique=True)
    sector = models.CharField(max_length=255)
    srg = models.CharField(max_length=255, null=True, blank=True)
    comm_structure = models.CharField(max_length=255, null=True, blank=True)
    created_dt = models.DateTimeField()
    modified_dt = models.DateTimeField()
    multipolygon = models.MultiPolygonField()
    income = models.IntegerField(default=0)
    objects = CommunityManager()

    def __str__(self):
        return self.name


class CrimesReport(models.Model):
    category = models.CharField(max_length=50)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, blank=True, null=True
    )
    january = models.IntegerField(default=0, null=True, blank=True)
    february = models.IntegerField(null=True, blank=True)
    march = models.IntegerField(null=True, blank=True)
    april = models.IntegerField(null=True, blank=True)
    may = models.IntegerField(null=True, blank=True)
    june = models.IntegerField(null=True, blank=True)
    july = models.IntegerField(null=True, blank=True)
    august = models.IntegerField(null=True, blank=True)
    september = models.IntegerField(null=True, blank=True)
    october = models.IntegerField(null=True, blank=True)
    november = models.IntegerField(null=True, blank=True)
    december = models.IntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.community_name


class Service(models.Model):
    TYPE_CHOICES = [
        ("Community Centre", "Community Centre"),
        ("Attraction", "Attraction"),
        ("Library", "Library"),
        ("Court", "Court"),
        ("Hospital", "Hospital"),
        ("PHS Clinic", "PHS Clinic"),
        ("Commercial", "Commercial"),
        ("Visitor Info", "Visitor Info"),
        ("Social Dev Ctr", "Social Dev Ctr"),
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    comm_code = models.CharField(max_length=10)
    point = models.PointField()  # 需要安装 django.contrib.gis

    def __str__(self):
        return self.name


class Income(models.Model):
    ward = models.CharField(max_length=255)
    total_household_total_income = models.IntegerField()
    under_20_000 = models.IntegerField()
    _20_000_to_39_999 = models.IntegerField()
    _40_000_to_59_999 = models.IntegerField()
    _60_000_to_79_999 = models.IntegerField()
    _80_000_to_99_999 = models.IntegerField()
    _100_000_to_124_999 = models.IntegerField()
    _125_000_to_149_999 = models.IntegerField()
    _150_000_to_199_999 = models.IntegerField()
    _200_000_and_over = models.IntegerField()
    polygon = models.MultiPolygonField()

    # def __str__(self):
    #     return self.ward
