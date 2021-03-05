from django.db import connection
from drf_yasg import openapi

from api.functions import fetch_cats
from api.serializers import CatSerializer

info = openapi.Info(
    title="Cats API",
    default_version="v1",
)

order_by_param = openapi.Parameter(
    'order_by',
    openapi.IN_QUERY,
    description="For sorting. Prepend with a `-` for descending order.",
    type=openapi.TYPE_STRING,
)

limit = openapi.Parameter(
    'limit',
    openapi.IN_QUERY,
    description="For getting a subset of the result rows.",
    type=openapi.TYPE_INTEGER,
)

offset = openapi.Parameter(
    'offset',
    openapi.IN_QUERY,
    description="For setting a row starting from which the results will be returned.",
    type=openapi.TYPE_INTEGER,
)

with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM cats LIMIT 3;')
    some_cats = [cat._asdict() for cat in fetch_cats(cursor)]

get_response = openapi.Response(
    'OK',
    schema=CatSerializer(many=True),
    examples={'application/json': some_cats},
)
