from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedMixin
from performance.models import Performance
from enum import Enum


class ReportReason(Enum):
    SPAM = ('spam', '스팸, 도배글')
    ADVERTISEMENT = ('advertisement', '홍보, 영리목적')
    ABUSIVE = ('abusive', '욕설, 비방글')
    OTHER = ('other', '기타')

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        return [(reason.value, reason.label) for reason in cls]

    @classmethod
    def get_label(cls, value):
        """value에 해당하는 레이블을 반환"""
        for reason in cls:
            if reason.value == value:
                return reason.label
        return None


class Review(TimeStampedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="작성자")
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="reviews", verbose_name="공연")
    content = models.CharField(max_length=280, null=False, blank=False, verbose_name="리뷰 내용")
    reported_user = models.ManyToManyField(User, through="ReviewReport", blank=True, verbose_name='리뷰 신고한 유저')

    def __str__(self):
        return f"Review by {self.user.username} on {self.performance.name}"

    class Meta:
        db_table = "review"
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'


class ReviewReport(TimeStampedMixin):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_reviews",)
    reason = models.CharField(
        max_length=20,
        choices=ReportReason.choices(),
        default=ReportReason.SPAM.value,
    )
    other_reason = models.CharField(max_length=500, blank=True, null=True)  # '기타' 사유 입력 필드

    class Meta:
        verbose_name = 'Review Report'
        verbose_name_plural = 'Review Reports'

    def __str__(self):
        return f'Report for review {self.review.id} by user {self.user.id}'

    class Meta:
        db_table = "review_report"
        verbose_name = '리뷰 신고 현황'
        verbose_name_plural = '리뷰 신고 현황'