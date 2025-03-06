from rest_framework import viewsets, mixins, permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.paginations import StandardResultsSetPagination
from .models import Performance
from .serializers import PerformanceSerializer


class PerformanceViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """공연 리스트 및 상세 조회 API"""
    serializer_class = PerformanceSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Performance.objects.select_related('genre').prefetch_related('liked_users').all()
        genre_id = self.request.query_params.get('genre_id', None)
        status = self.request.query_params.get('status', None)

        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class PerformanceLikeView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """마이페이지 - 좋아요한 공연 목록"""
        queryset = Performance.objects.prefetch_related('liked_users').filter(liked_users__user_id=request.user.id)
        sort_by = kwargs.get('sort_by', 'like_created')

        if sort_by == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-liked_users__created_at')  # 기본값은 liked_users의 created_at 기준으로 정렬

        serializer = PerformanceSerializer(queryset, many=True, read_only=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """공연 좋아요/좋아요 취소 API"""

        performance_id = request.GET.get('performance_id', None)
        if not performance_id:
            return Response({"detail": "performance_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        performance = get_object_or_404(Performance, id=performance_id)
        like, created = performance.liked_users.get_or_create(user=request.user)
        status_code = status.HTTP_201_CREATED

        if not created:
            like.delete()
            status_code=status.HTTP_200_OK

        serializer = PerformanceSerializer(performance, context={'request': request})
        return Response(serializer.data, status=status_code)

