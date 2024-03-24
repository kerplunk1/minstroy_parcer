import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import settings


conn = psycopg2.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASS, host=settings.DB_HOST, port=settings.DB_POTR)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# cur.execute("SELECT COUNT(DISTINCT url) FROM urls WHERE parse_date = CURRENT_DATE;")
cur.execute("SELECT * FROM urls")
# cur.execute("TRUNCATE urls")

records = cur.fetchall()
for i in records:
    print(i)