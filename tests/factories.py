import factory
import faker
from datetime import date, timedelta
from random import choice
from django.contrib.auth.models import User
from performance.models import Genre, Performance, PerformanceLike
from review.models import Review, ReviewReport, ReportReason


fake = faker.Faker("ko_KR")

class UserFactory(factory.django.DjangoModelFactory):
    """유저 Factory"""
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class GenreFactory(factory.django.DjangoModelFactory):
    """공연 장르 Factory"""
    class Meta:
        model = Genre

    name = factory.Faker("word", locale="ko_KR")


class PerformanceFactory(factory.django.DjangoModelFactory):
    """공연 Factory"""
    class Meta:
        model = Performance

    genre = factory.SubFactory(GenreFactory)
    code = factory.LazyAttribute(lambda _: f"CODE-{fake.unique.random_int(1000, 9999)}")
    name = factory.Faker("sentence", nb_words=3, locale="ko_KR")  # 랜덤 문장 (공연명)
    price = factory.LazyAttribute(lambda _: fake.random_int(70000, 200000))  # 7만~20만 랜덤 가격
    started_at = factory.LazyFunction(lambda: date.today())
    ended_at = factory.LazyFunction(lambda: date.today() + timedelta(days=30))


class PerformanceLikeFactory(factory.django.DjangoModelFactory):
    """공연 좋아요 Factory"""

    class Meta:
        model = PerformanceLike

    user = factory.SubFactory(UserFactory)
    performance = factory.SubFactory(PerformanceFactory)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    performance = factory.SubFactory(PerformanceFactory)
    content = factory.Faker("sentence", locale="ko_KR")


class ReviewReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReviewReport

    user = factory.SubFactory(UserFactory)
    review = factory.SubFactory(ReviewFactory)
    reason = factory.LazyAttribute(lambda _: choice([reason.value for reason in ReportReason]))  # Enum에서 무작위 값 선택
    other_reason = factory.Faker("sentence", locale="ko_KR")