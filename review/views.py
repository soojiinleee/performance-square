from rest_framework import viewsets, permissions, status, generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from core.permissions import IsOwnerOrReadOnly
from core.paginations import StandardCursorPagination
from .models import Review
from .serializers import ReviewSerializer, CreateReviewSerializer, UpdateReviewSerializer, CreateReviewReportSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """공연 후기 CRUD API"""
    pagination_class = StandardCursorPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['performance__name']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = (Review.objects.select_related('user', 'performance', 'performance__genre')
                    .prefetch_related('reported_user')
                    .annotate(report_count=Count('reported_user'))
                    .all())

        # list 조회인 경우
        author_id = self.request.query_params.get('author_id', None)
        performance_id = self.request.query_params.get('performance_id', None)
        is_my_review = self.request.query_params.get('is_my_review', False)

        # 리뷰 목록 페이지
        if author_id:       # 리뷰 작성자의 모든 리뷰 조회
            queryset = queryset.filter(user__id=author_id)
        if performance_id:  # 특정 공연의 모든 리뷰 조회
            queryset = queryset.filter(performance__id=performance_id)

        # 마이페이지 - 리뷰 목록 : 본인이 작성한 리뷰만 조회
        if is_my_review:
            queryset = queryset.filter(user__id=self.request.user.id).filter(report_count__lt=5)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReviewSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateReviewSerializer
        return ReviewSerializer


class ReviewReportAPIView(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateReviewReportSerializer

    def post(self, request, *args, **kwargs):
        """리뷰 신고 API"""

        review_id = request.data.get('review')
        get_object_or_404(Review, id=review_id)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)