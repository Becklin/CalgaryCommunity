from django.contrib import admin
from .models import Community, CrimesReport, Service

# Register your models here.

admin.site.register(Community)
admin.site.register(CrimesReport)
admin.site.register(Service)
