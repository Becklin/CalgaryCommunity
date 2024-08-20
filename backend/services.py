from django.db import connection


def fetch_crimes_reports():
    sql = """
        SELECT community_id, 
               SUM(whole_year) AS total_whole_year
        FROM (
            SELECT community_id, 
                   category, 
                   SUM(january + february + march + april + may + june + july + august + september + october + november + december) AS whole_year
            FROM backend_crimesreport
            GROUP BY community_id, category
        ) AS subquery
        GROUP BY community_id
        ORDER BY community_id;
        """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()

        # 构建结果列表
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in results]
