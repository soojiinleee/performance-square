import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient

from tests.factories import (
    PerformanceFactory,
    GenreFactory,
    UserFactory,
    PerformanceLikeFactory,
    ReviewFactory,
    ReviewReportFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    # 테스트용 유저 생성
    user1 = UserFactory.create(
        username="user1", email="user1@test.com", password="user1"
    )
    user2 = UserFactory.create(
        username="user2", email="user2@test.com", password="user2"
    )
    user3 = UserFactory.create(
        username="user3", email="user3@test.com", password="user3"
    )
    user4 = UserFactory.create(
        username="user4", email="user4@test.com", password="user4"
    )
    user5 = UserFactory.create(
        username="user5", email="user5@test.com", password="user5"
    )

    return {
        "user1": user1,
        "user2": user2,
        "user3": user3,
        "user4": user4,
        "user5": user5,
    }


@pytest.fixture
def genre_data(db):
    """장르 데이터"""
    musical = GenreFactory.create(name="뮤지컬")
    classical = GenreFactory.create(name="클래식")
    pop = GenreFactory.create(name="대중음악")

    return {"musical": musical, "classical": classical, "pop": pop}


@pytest.fixture
def performance_data(db, genre_data):
    """공연 필터링 & 상세 테스트 데이터"""
    performance1 = PerformanceFactory.create(
        genre=genre_data["musical"],
        name="오페라의 유령",
        price=150000,
        started_at=date.today() - timedelta(days=60),
        ended_at=date.today() + timedelta(days=30),
    )  # 공연 중
    performance2 = PerformanceFactory.create(
        genre=genre_data["classical"],
        name="베토벤 교향곡",
        price=120000,
        started_at=date.today() - timedelta(days=32),
        ended_at=date.today() - timedelta(days=30),
    )  # 종료
    performance3 = PerformanceFactory.create(
        genre=genre_data["musical"],
        name="지킬앤하이드",
        price=160000,
        started_at=date.today() - timedelta(days=30),
        ended_at=date.today() + timedelta(days=30),
    )  # 공연 중
    performance4 = PerformanceFactory.create(
        genre=genre_data["pop"],
        name="BlankPink Tour : Seoul",
        price=130000,
        started_at=date.today() + timedelta(days=30),
        ended_at=date.today() + timedelta(days=32),
    )  # 예정
    performance5 = PerformanceFactory.create(
        genre=genre_data["musical"],
        name="위키드",
        price=180000,
        started_at=date.today() + timedelta(days=40),
        ended_at=date.today() + timedelta(days=70),
    )  # 예정

    return {
        "performance1": performance1,
        "performance2": performance2,
        "performance3": performance3,
        "performance4": performance4,
        "performance5": performance5,
    }


@pytest.fixture
def performance_pagination_data(db, genre_data):
    """공연 목록 페이지네이션 테스트"""
    return PerformanceFactory.create_batch(30)


@pytest.fixture
def performance_likes_data(db, performance_data, user_data):
    """공연 좋아요 테스트 : 뮤지컬 장르만"""
    like1 = PerformanceLikeFactory.create(
        user=user_data["user1"], performance=performance_data["performance1"]
    )
    like2 = PerformanceLikeFactory.create(
        user=user_data["user2"], performance=performance_data["performance1"]
    )
    like3 = PerformanceLikeFactory.create(
        user=user_data["user1"], performance=performance_data["performance5"]
    )
    like4 = PerformanceLikeFactory.create(
        user=user_data["user2"], performance=performance_data["performance2"]
    )

    return {
        "like1": like1,
        "like2": like2,
        "like3": like3,
        "like4": like4,
    }


@pytest.fixture
def review_data(db, performance_data, user_data):
    """공연 별 리뷰 데이터"""
    review1 = ReviewFactory.create(
        user=user_data["user1"],
        performance=performance_data["performance1"],
        content="재밌어요1",
    )
    review2 = ReviewFactory.create(
        user=user_data["user2"],
        performance=performance_data["performance1"],
        content="재밌어요2",
    )
    review3 = ReviewFactory.create(
        user=user_data["user3"],
        performance=performance_data["performance1"],
        content="재밌어요3",
    )
    review4 = ReviewFactory.create(
        user=user_data["user1"],
        performance=performance_data["performance2"],
        content="재밌어요4",
    )
    review5 = ReviewFactory.create(
        user=user_data["user1"],
        performance=performance_data["performance3"],
        content="재밌어요5",
    )
    review6 = ReviewFactory.create(
        user=user_data["user2"],
        performance=performance_data["performance3"],
        content="재밌어요6",
    )
    review7 = ReviewFactory.create(
        user=user_data["user3"],
        performance=performance_data["performance3"],
        content="♣︎V.I.P로 모십니다♣︎ 지금 가입하기 ▶︎▶︎▶︎ 'https://strange.vip.com' ◀︎◀︎◀︎",
    )

    return {
        "review1": review1,
        "review2": review2,
        "review3": review3,
        "review4": review4,
        "review5": review5,
        "review6": review6,
        "review7": review7,
    }


@pytest.fixture
def review_report_data(db, review_data, user_data):
    """리뷰 신고 데이터"""
    report1 = ReviewReportFactory.create(
        user=user_data["user1"], review=review_data["review7"], reason="spam"
    )
    report2 = ReviewReportFactory.create(
        user=user_data["user2"], review=review_data["review7"], reason="spam"
    )
    report3 = ReviewReportFactory.create(
        user=user_data["user3"], review=review_data["review7"], reason="spam"
    )
    report4 = ReviewReportFactory.create(
        user=user_data["user4"], review=review_data["review7"], reason="spam"
    )
    report5 = ReviewReportFactory.create(
        user=user_data["user5"], review=review_data["review7"], reason="spam"
    )

    return {
        "report1": report1,
        "report2": report2,
        "report3": report3,
        "report4": report4,
        "report5": report5,
    }
