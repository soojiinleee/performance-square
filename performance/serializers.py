from rest_framework import serializers
from .models import Performance, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class PerformanceSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = ['id', 'genre', 'name', 'status', 'price', 'started_at', 'ended_at', 'like_count', 'is_liked']

    def get_like_count(self, obj):
        """공연의 좋아요 수"""
        return obj.liked_users.count()

    def get_is_liked(self, obj):
        """로그인한 유저가 공연에 좋아요 표시 했는지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(user=request.user).exists()
        return False
