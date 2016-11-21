from rest_framework import serializers
from .models import News, Category


class NewsSerializer(serializers.Serializer):
    category = serializers.CharField()
    creation_date = serializers.DateTimeField()
    title = serializers.CharField()
    text = serializers.CharField()

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data['category']
        instance.title = validated_data['title']
        instance.text = validated_data['text']
        instance.save()
        return instance

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("O título deve ter no mínimo 3 caracteres")
        return value.strip()


class NewsModelSerializer(serializers.ModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = News
        fields = ('title', 'creation_date', 'title', 'text', 'url',)
        read_only_fields = ('creation_date', 'url',)


class CategoryModelSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'url',)