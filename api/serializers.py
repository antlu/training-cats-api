from rest_framework import serializers


class CatSerializer(serializers.Serializer):
    name = serializers.CharField()
    color = serializers.CharField()
    tail_length = serializers.IntegerField(min_value=0)
    whiskers_length = serializers.IntegerField(min_value=0)
