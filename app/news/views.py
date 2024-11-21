from rest_framework import generics
from .models import NewsCategory, News
from .serializers import NewsCategorySerializer, NewsSerializer


# API for fetching all categories
class NewsCategoryList(generics.ListAPIView):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer


# API for fetching all news in a specific category
class NewsByCategoryList(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return News.objects.filter(category_id=category_id)


class LatestNewsView(generics.ListAPIView):
    queryset = News.objects.order_by("-created_at")[:10]
    serializer_class = NewsSerializer
