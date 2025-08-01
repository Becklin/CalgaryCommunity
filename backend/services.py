from django.db import connection
from django.contrib.gis.geos import MultiPolygon
from decimal import Decimal
from .models import fetch_crimes_reports, Community, NormalizedDataCache
from decimal import Decimal
import datetime


class RankingService:
    def __init__(self, crimes_weight, services_weight, income_weight):
        self.crime_weight = crimes_weight / 10
        self.service_weight = services_weight / 10
        self.income_weight = income_weight / 10

    def convert_special_types(self, obj):
        if isinstance(obj, dict):
            return {k: self.convert_special_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_special_types(i) for i in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj

    def get_normalized_data_from_db_or_compute(self):
        cache_key = "normalized_data"

        try:
            cache_obj = NormalizedDataCache.objects.get(key=cache_key)
            data = cache_obj.data
        except NormalizedDataCache.DoesNotExist:
            print("trigger fetch")
            records = fetch_crimes_reports()
            communities = list(Community.objects.all().values())
            services = Community.objects.services_within_5km()
            for comm in communities:
                polygon = comm.get("multipolygon")
                if isinstance(polygon, MultiPolygon):
                    comm["multipolygon"] = polygon.geojson
                    # serialize type of point
                    comm["centroid"] = {
                        "type": "Point",
                        "coordinates": [polygon.centroid.x, polygon.centroid.y],
                    }

            community_dict = {comm["id"]: comm for comm in communities}

            community_ids = set(community_dict.keys())
            record_ids = {record["community_id"] for record in records}

            # Remove missing ids
            missing_ids = community_ids - record_ids
            for id in missing_ids:
                community_dict.pop(id, None)
                services.pop(id, None)
            # Normalize
            min_service = min([y for x, y in services.items()])
            max_service = max([y for x, y in services.items()])
            # Normalize incomes eg.  {'id': 113, 'class_name': 'Residential', 'class_code': '1'}
            min_income = min(communities, key=lambda x: x.get("income")).get("income")
            max_income = max(communities, key=lambda x: x.get("income")).get("income")
            # Normalize crime records eg. {'community_id': 0, 'total_whole_year': Decimal('2')}
            min_record = min(records, key=lambda x: x["total_whole_year"]).get(
                "total_whole_year"
            )
            max_record = max(records, key=lambda x: x["total_whole_year"]).get(
                "total_whole_year"
            )

            services_normalized = {
                k: (
                    (v - min_service) / (max_service - min_service)
                    if max_service > min_service
                    else 0
                )
                for k, v in services.items()
            }

            incomes_normalized = {
                comm["id"]: (
                    (comm["income"] - min_income) / (max_income - min_income)
                    if max_income > min_income
                    else 0
                )
                for comm in communities
            }

            records_normalized = {
                r["community_id"]: (
                    1
                    - ((r["total_whole_year"] - min_record) / (max_record - min_record))
                    if max_record > min_record
                    else 0
                )
                for r in records
            }
            data = {
                "normalized_services": services_normalized,
                "normalized_income": incomes_normalized,
                "normalized_records": records_normalized,
                "records": records,
                "communities": communities,
                "services": services,
            }
            ## Your data dictionary contains Decimal objects (likely from numeric fields retrieved from the database).
            # When you use update_or_create(..., defaults={"data": data}) to write this data into a JSONField,
            # Django internally uses json.dumps() to serialize it.
            # However, json.dumps() cannot directly serialize Decimal types, which causes the error.
            data = self.convert_special_types(data)
            NormalizedDataCache.objects.update_or_create(
                key=cache_key, defaults={"data": data}
            )
        return data

    def calculate_scores(self):
        # CACHE DATA
        normalized_data = self.get_normalized_data_from_db_or_compute()
        communities = normalized_data["communities"]
        services = normalized_data["services"]
        records = normalized_data["records"]
        services_normalized = normalized_data["normalized_services"]
        incomes_normalized = normalized_data["normalized_income"]
        records_normalized = normalized_data["normalized_records"]

        # calculate scores based on weights
        for comm in communities:
            comm_id = comm["id"]
            s = services_normalized.get(comm_id, 0)
            i = incomes_normalized.get(comm_id, 0)
            r = float(records_normalized.get(comm_id, 0))

            comm["score"] = (
                (s * self.service_weight)
                + (r * self.crime_weight)
                + (i * self.income_weight)
            )
            comm["service_count"] = services.get(comm_id, 0)
            comm["crimes_count"] = next(
                (
                    rec["total_whole_year"]
                    for rec in records
                    if rec["community_id"] == comm_id
                ),
                0,
            )

        # generate sorted data for view
        result = sorted(
            [
                {
                    "id": comm["id"],
                    "type": comm["class_name"],
                    "name": comm["name"],
                    "sector": comm["sector"],
                    "multipolygon": comm["multipolygon"],
                    "income": comm["income"],
                    "centroid": comm["centroid"],
                    "score": comm["score"],
                    "service_count": comm["service_count"],
                    "crimes_count": comm["crimes_count"],
                }
                for comm in communities
            ],
            key=lambda x: x["score"],
            reverse=True,
        )
        return result
