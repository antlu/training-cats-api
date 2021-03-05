from django.db import DataError, IntegrityError, ProgrammingError, connection
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from psycopg2.errors import UndefinedColumn
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

from api.exceptions import BadRequest
from api.functions import build_query, fetch_cats, get_valid_params
from api.openapi import get_response, limit, offset, order_by_param
from api.serializers import CatSerializer
from api.throttling import AllUsersRateThrottle


def ping(request):
    return HttpResponse("Cats Service. Version 0.1", content_type='text/plain')


@swagger_auto_schema(
    method='get',
    manual_parameters=[order_by_param, limit, offset],
    responses={status.HTTP_200_OK: get_response},
)
@swagger_auto_schema(
    method='post',
    responses={400: get_response},
    request_body=CatSerializer,
)
@api_view(['GET', 'POST'])
@throttle_classes([AllUsersRateThrottle])
def cats_list(request):
    if request.method == 'GET':
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
            cats = fetch_cats(cursor)
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    serializer = CatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                'INSERT INTO cats VALUES'
                '(%(name)s, %(color)s, %(tail_length)s, %(whiskers_length)s)',
                serializer.validated_data,
            )
        except IntegrityError as exc:
            raise BadRequest(str(exc), 'integrity_error')
    return Response(serializer.data, status=status.HTTP_201_CREATED)
