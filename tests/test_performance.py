import pytest

from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPerformancePagination:
    """공연 목록 조회 페이지네이션 테스트 : 30개 공연 데이터로 테스트"""

    def setup_method(self, method):
        self.url = reverse("performance-list")

    def test_default_pagination(self, api_client, performance_pagination_data):
        """기본 페이지네이션 (page=1) 테스트"""
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert "Next-Page" in response.headers
        assert "Total-Count" in response.headers
        assert int(response.headers["Total-Count"]) == len(performance_pagination_data)
        assert len(response.json()) == 20

    def test_second_page_pagination(self, api_client, performance_pagination_data):
        """두 번째 페이지 요청 (page=2) 테스트"""
        response = api_client.get(self.url, {"page": 2})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 10  # 남은 10개 공연 확인
        assert "Previous-Page" in response.headers

    def test_custom_page_size(self, api_client, performance_pagination_data):
        """`page_size=5`로 변경해서 요청 테스트"""
        response = api_client.get(self.url, {"page": 2, "page_size": 5})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5  # `page_size=5` 적용 확인
        assert "Next-Page" in response.headers
        assert "Previous-Page" in response.headers

    def test_custom_page_number(self, api_client, performance_pagination_data):
        """특정 페이지 요청 테스트 : 마지막 페이지"""
        response = api_client.get(self.url, {"page": "last"})

        assert response.status_code == status.HTTP_200_OK
        assert "Next-Page" not in response.headers
        assert "Previous-Page" in response.headers


@pytest.mark.django_db
class TestPerformanceListFilter:
    """공연 목록 필터링 테스트"""

    def setup_method(self, method):
        self.url = reverse("performance-list")

    # @pytest.mark.django_db
    def test_filter_by_genre(self, api_client, performance_data, genre_data):
        """장르별 공연 목록 필터링 테스트"""
        response = api_client.get(self.url, {"genre_id": genre_data["musical"].id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3
        assert response.json()[0]["name"] == "오페라의 유령"

    # @pytest.mark.django_db
    def test_filter_by_status(self, api_client, performance_data):
        """상태별 공연 목록 필터링 테스트"""
        response = api_client.get(self.url, {"status": "upcoming"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2


@pytest.mark.django_db
class TestPerformanceListFilter:
    """공연 상세 조회 테스트"""

    # @pytest.mark.django_db
    def test_retrieve_performance(self, api_client, performance_data):
        """존재하는 공연 상세 조회 테스트"""
        url = reverse("performance-detail", args=[performance_data["performance1"].id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "오페라의 유령"
        assert response.json()["price"] == 150000
        assert response.json()["genre"]["name"] == "뮤지컬"

    # @pytest.mark.django_db
    def test_retrieve_nonexistent_performance(self, api_client):
        """존재하지 않는 공연 조회 시 404 반환 테스트"""
        url = reverse("performance-detail", args=[999])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPerformanceLike:

    def test_create_performance_like(self, api_client, user_data, performance_data):
        """공연 좋아요 등록 테스트"""
        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username="user1")
        api_client.force_authenticate(user=user)

        # when : 공연 좋아요 API 호출
        url = reverse("performance-like")
        response = api_client.post(
            f"{url}?performance_id={performance_data['performance1'].id}"
        )

        # then : 좋아요가 성공적으로 생성되었는지 확인
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == performance_data["performance1"].name
        assert response.json()["is_liked"] is True

    def test_cancel_performance_like(self, api_client, user_data, performance_data):
        """공연 좋아요 취소 테스트"""
        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username="user1")
        api_client.force_authenticate(user=user)

        # when : 공연 좋아요 API 호출 (좋아요 생성)
        url = reverse("performance-like")
        api_client.post(f"{url}?performance_id={performance_data['performance1'].id}")

        # 공연 좋아요 취소 API 호출 (같은 공연에 대해 취소)
        response = api_client.post(
            f"{url}?performance_id={performance_data['performance1'].id}"
        )

        # 좋아요 취소 되었는지 확인
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == performance_data["performance1"].name
        assert response.json()["is_liked"] is False

    def test_performance_like_count_with_anonymouse(
        self, api_client, genre_data, performance_likes_data
    ):
        """공연의 좋아요 조회 : 로그인 안 한 경우"""

        # when : 공연 목록 조회 API 호출
        url = reverse("performance-list")
        response = api_client.get(url, {"genre_id": genre_data["musical"].id})

        # then : 공연 좋아요 수 확인
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["name"] == "오페라의 유령"
        assert response.json()[0]["like_count"] == 2
        assert response.json()[0]["is_liked"] is False
        assert response.json()[1]["name"] == "지킬앤하이드"
        assert response.json()[1]["like_count"] == 0
        assert response.json()[1]["is_liked"] is False
        assert response.json()[2]["name"] == "위키드"
        assert response.json()[2]["like_count"] == 1
        assert response.json()[2]["is_liked"] is False

    def test_performance_liked_with_auth_user(
        self, api_client, genre_data, performance_likes_data
    ):
        """공연 좋아요 조회 : 로그인 한 경우"""
        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username="user1")
        api_client.force_authenticate(user=user)

        # when : 공연 목록 조회 API 호출
        url = reverse("performance-list")
        response = api_client.get(url, {"genre_id": genre_data["musical"].id})

        # then : 공연 좋아요 수 및 본인이 좋아요 했는지 확인
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["name"] == "오페라의 유령"
        assert response.json()[0]["like_count"] == 2
        assert response.json()[0]["is_liked"] is True
        assert response.json()[1]["name"] == "지킬앤하이드"
        assert response.json()[1]["like_count"] == 0
        assert response.json()[1]["is_liked"] is False
        assert response.json()[2]["name"] == "위키드"
        assert response.json()[2]["like_count"] == 1
        assert response.json()[2]["is_liked"] is True

    def test_liked_performance_list_by_anonymouse(self, api_client):
        """마이페지 - 좋아요 공연 목록 : 로그인 안 한 유저"""
        url = reverse("performance-like")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_liked_performance_list_by_auth_user(
        self, api_client, performance_likes_data
    ):
        """마이페이지 - 좋아요 공연 목록 : 로그인 유저"""
        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username="user1")
        api_client.force_authenticate(user=user)

        # when : 공연 목록 조회 API 호출
        url = reverse("performance-like")
        response = api_client.get(url)

        # then : 최근 좋아요한 공연 순으로 정렬
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "위키드"

    def test_ordered_liked_performance_list(self, api_client, performance_likes_data):
        """마이페이지 - 좋아요 공연 목록 정렬"""
        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username="user2")
        api_client.force_authenticate(user=user)

        # when : 공연 목록 조회 API 호출
        url = reverse("performance-like")
        response = api_client.get(url, {"sort_by": "name"})

        # then : 공연 이름 순으로 정렬
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "베토벤 교향곡"
