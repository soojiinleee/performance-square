from datetime import datetime
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Case, When, Value, CharField
from core.models import TimeStampedMixin


class PerformanceStatus(Enum):
    UPCOMING = "upcoming"  # 예정
    ONGOING = "ongoing"  # 공연 중
    ENDED = "ended"  # 종료


class Genre(TimeStampedMixin):
    name = models.CharField(max_length=100, verbose_name="이름")

    class Meta:
        db_table = "performance_genre"
        verbose_name = "장르"
        verbose_name_plural = "장르"

    def __str__(self):
        return self.name


class PerformanceManager(models.Manager):
    def get_queryset(self):
        today = datetime.today().date()
        return (
            super()
            .get_queryset()
            .annotate(
                status=Case(
                    When(
                        started_at__lte=today,
                        ended_at__gte=today,
                        then=Value(PerformanceStatus.ONGOING.value),
                    ),
                    When(ended_at__lt=today, then=Value(PerformanceStatus.ENDED.value)),
                    default=Value(PerformanceStatus.UPCOMING.value),
                    output_field=CharField(),
                )
            )
        )


class Performance(TimeStampedMixin):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="performances",
        verbose_name="장르",
    )
    code = models.CharField(max_length=100, unique=True, verbose_name="KOPIS 공연ID")
    name = models.CharField(max_length=255, verbose_name="공연명")
    price = models.IntegerField(verbose_name="티켓 가격", null=False, default=0)
    started_at = models.DateField(verbose_name="공연 시작일")
    ended_at = models.DateField(verbose_name="공연 종료일")
    user = models.ManyToManyField(
        User, through="PerformanceLike", verbose_name="좋아요 클릭한 유저: m2m"
    )

    objects = PerformanceManager()

    class Meta:
        db_table = "performance"
        verbose_name = "공연"
        verbose_name_plural = "공연"
        ordering = ["ended_at"]

    def __str__(self):
        return self.name


class PerformanceLike(TimeStampedMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked_performances"
    )
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="liked_users"
    )

    class Meta:
        db_table = "performance_like"
        verbose_name = "공연_좋아요"
        verbose_name_plural = "공연_좋아요"
        unique_together = ("user", "performance")
