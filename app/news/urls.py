from django.urls import path
from .views import NewsCategoryList, NewsByCategoryList, LatestNewsView


urlpatterns = [
    path("categories/", NewsCategoryList.as_view(), name="news-category-list"),
    path(
        "categories/<uuid:category_id>/news/",
        NewsByCategoryList.as_view(),
        name="news-by-category",
    ),
    path("latest/", LatestNewsView.as_view(), name="latest-news"),
]
