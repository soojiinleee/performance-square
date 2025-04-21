from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PerformanceViewSet, PerformanceLikeView

router = SimpleRouter()
router.register(r"", PerformanceViewSet, basename="performance")

urlpatterns = [
    path("like/", PerformanceLikeView.as_view(), name="performance-like"),
    path("", include(router.urls)),
]
