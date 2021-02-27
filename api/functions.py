from collections import namedtuple

from psycopg2.sql import Identifier, SQL


def fetch_all_cats(cursor):
    columns = [col[0] for col in cursor.description]
    Cat = namedtuple('Cat', columns)
    return [Cat(*row) for row in cursor.fetchall()]


param_SQL_mapping = {
    'order_by': 'ORDER BY {field} {direction}',
    'limit': 'LIMIT %(limit)s',
    'offset': 'OFFSET %(offset)s',
}


def build_query(table, params):
    base = 'SELECT * FROM {table}'
    clauses = [
        param_SQL_mapping[param]
        for param in param_SQL_mapping
        if param in params
    ]
    return SQL(' '.join([base, *clauses])).format(
        table=Identifier(table),
        field=Identifier(params.get('order_by', '')),
        direction=SQL(params.get('direction', '')),
    )


def get_valid_params(query_params):
    legit_params = param_SQL_mapping.keys()
    params = {
        param: query_params[param]
        for param in query_params
        if param in legit_params
    }
    ordering = query_params.get('order_by')
    if ordering:
        if ordering.startswith('-'):
            norm_ordering = {'order_by': ordering[1:], 'direction': 'DESC'}
        else:
            norm_ordering = {'order_by': ordering, 'direction': 'ASC'}
        return params | norm_ordering
    return params
