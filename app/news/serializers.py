from rest_framework import serializers
from .models import NewsCreator, NewsCategory, News


class NewsCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCreator
        fields = "__all__"


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    creator = NewsCreatorSerializer()
    category = NewsCategorySerializer()

    class Meta:
        model = News
        fields = "__all__"
