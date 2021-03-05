from django.db import connection
from rest_framework import serializers

with connection.cursor() as cursor:
    cursor.execute('SELECT DISTINCT color FROM cats;')
    COLORS = tuple(color for row in cursor.fetchall() for color in row)


class CatSerializer(serializers.Serializer):
    name = serializers.CharField()
    color = serializers.CharField()
    tail_length = serializers.IntegerField(min_value=0)
    whiskers_length = serializers.IntegerField(min_value=0)

    class Meta:

        swagger_schema_fields = {
            'example': {
                'name': 'Pushok',
                'color': 'white',
                'tail_length': 30,
                'whiskers_length': 10,
            },
        }

    def validate_name(self, value):
        if value.isnumeric():
            raise serializers.ValidationError("Name must start with a letter.")
        return value

    def validate_color(self, value):
        if value not in COLORS:
            raise serializers.ValidationError("Unknown color.")
        return value
