from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class Community(models.Model):
    class_code = models.CharField(max_length=50)
    comm_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255, unique=True)
    sector = models.CharField(max_length=255)
    srg = models.CharField(max_length=255, null=True, blank=True)
    comm_structure = models.CharField(max_length=255, null=True, blank=True)
    created_dt = models.DateTimeField()
    modified_dt = models.DateTimeField()
    multipolygon = models.MultiPolygonField()

    def __str__(self):
        return self.name


class CrimesReport(models.Model):
    category = models.CharField(max_length=50)
    community_name = models.ForeignKey(
        Community, to_field="name", on_delete=models.CASCADE
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

    def __str__(self):
        return self.name
