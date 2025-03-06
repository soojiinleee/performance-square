from rest_framework import serializers

from performance.serializers import PerformanceSerializer
from user.serializers import UserSerializer
from review.models import Review, ReviewReport


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    performance = PerformanceSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'performance', 'content', 'created_at', 'updated_at']

    def get_content(self, obj):
        if obj.report_count >= 5:
            return "신고된 리뷰입니다"
        return obj.content

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['performance', 'content']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)

class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['content']


class CreateReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReport
        fields = ['review', 'reason', 'other_reason']

    def validate(self, attrs):
        """리뷰 중복 신고 확인"""

        review = attrs.get('review')
        user = self.context['request'].user

        if ReviewReport.objects.filter(review=review, user=user).exists():
            raise serializers.ValidationError({"detail": "이미 신고한 리뷰입니다."})

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)