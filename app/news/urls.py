from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsCategoryViewSet

router = DefaultRouter()
router.register(r"categories", NewsCategoryViewSet, basename="newscategory")

urlpatterns = [
    path("", include(router.urls)),
]
