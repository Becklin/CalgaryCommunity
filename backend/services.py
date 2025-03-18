from django.db import connection
from django.contrib.gis.geos import MultiPolygon
from decimal import Decimal
from .models import fetch_crimes_reports, Community


class RankingService:
    def __init__(self, crimes_weight, services_weight, income_weight):
        self.crime_weight = crimes_weight / 10
        self.service_weight = services_weight / 10
        self.income_weight = income_weight / 10

    def calculate_scores(self):
        # prepare data
        records = fetch_crimes_reports()
        communities = list(Community.objects.all().values())
        services = Community.objects.services_within_5km()
        # print('服務', services)
        for comm in communities:
            polygon = comm.get("multipolygon")
            if isinstance(polygon, MultiPolygon):
                comm["multipolygon"] = polygon.geojson
                # serialize type of point
                comm["centroid"] = {
                    "type": "Point",
                    "coordinates": [polygon.centroid.x, polygon.centroid.y],
                }
        print('records', records)

        community_dict = {comm["id"]: comm for comm in communities}

        community_ids = set(community_dict.keys())
        record_ids = {record["community_id"] for record in records}
        # print('community_ids', community_ids)
        print('record_ids', record_ids)

        # Remove missing ids
        missing_ids = community_ids - record_ids
        for id in missing_ids:
            community_dict.pop(id, None)
            services.pop(id, None)
        print('服務', services)

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
                1 - ((r["total_whole_year"] - min_record) / (max_record - min_record))
                if max_record > min_record
                else 0
            )
            for r in records
        }
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
