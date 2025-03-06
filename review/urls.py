from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ReviewViewSet, ReviewReportAPIView

router = SimpleRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('report/', ReviewReportAPIView.as_view(), name='review-report'),
    path('', include(router.urls)),
]
