from rest_framework import serializers
from .models import News, NewsCategory, NewsCreator


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class NewsCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsCategory
        fields = "__all__"


class NewsCreatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsCreator
        fields = "__all__"
