from django.db import connection, DataError, ProgrammingError
from django.http import HttpResponse
from psycopg2.errors import UndefinedColumn
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.exceptions import BadRequest
from api.serializers import CatSerializer
from api.functions import build_query, fetch_all_cats, get_valid_params


def ping(request):
    return HttpResponse("Cats Service. Version 0.1", content_type='text/plain')


@api_view()
def cats_list(request):
    params = get_valid_params(request.query_params)
    with connection.cursor() as cursor:
        try:
            cursor.execute(build_query('cats', params), params)
        except ProgrammingError as exc:
            if isinstance(exc.__cause__, UndefinedColumn):
                raise BadRequest(str(exc), 'undefined_column')
            raise
        except DataError as exc:
            raise BadRequest(str(exc), 'data_error')
        cats = fetch_all_cats(cursor)
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)
