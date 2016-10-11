from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.Serializer):
    author = serializers.CharField()
    category = serializers.CharField()
    creation_date = serializers.DateTimeField()
    title = serializers.CharField()
    text = serializers.CharField()
