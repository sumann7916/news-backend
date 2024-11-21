from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import NewsCategory, News
from .serializers import NewsCategorySerializer, NewsSerializer
import logging


class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer

    @action(detail=True, methods=["get"], url_path="news")
    def get_news(self, request, pk=None):
        try:
            category = self.get_object()
            news = News.objects.filter(category=category)
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)
        except NewsCategory.DoesNotExist:
            logging.error("Category not found.")
            return Response({"error": "Category not found"}, status=404)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return Response(
                {"error": "An error occurred while fetching news."}, status=500
            )
