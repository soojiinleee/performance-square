import pytest

from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestReviewList:

    def setup_method(self, method):
        self.url = reverse('review-list')

    def test_specific_user_review_list(self, api_client, user_data, review_data):
        """특정 작성자의 리뷰 목록 조회 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user1')
        api_client.force_authenticate(user=user)

        # when : 리뷰 목록 조회 API 호출
        response = api_client.get(self.url, {"author_id":user_data["user2"].id})

        # then : 특정 유저가 작성한 리뷰 목록 반환
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        assert response.json()[0]["performance"]["name"] == "지킬앤하이드"

    def test_specific_performance_review_list(self, api_client, performance_data, review_data):
        """특정 공연의 리뷰 목록 조회 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user4')
        api_client.force_authenticate(user=user)

        # when : 리뷰 목록 조회 API 호출
        response = api_client.get(self.url, {"performance_id":performance_data["performance1"].id})

        # then : 특정 공연 리뷰 목록 반환
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3
        assert response.json()[0]["user"]["username"] == "user3"

    def test_my_review_list(self, api_client, review_data):
        """마이페이지 - 본인이 작성한 리뷰 조회 테스트 : 기본 정렬(최근 작성일 순)"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user1')
        api_client.force_authenticate(user=user)

        # when : 리뷰 목록 조회 API 호출
        response = api_client.get(self.url, {"is_my_review":True})

        # then : 리뷰 작성 순으로 정렬
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3
        assert response.json()[0]["performance"]["name"] == "지킬앤하이드"

    def test_ordered_my_review_list(self, api_client, review_data):
        """마이페이지 - 본인이 작성한 리뷰 조회 테스트 : 공연 이름 순 정렬"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user1')
        api_client.force_authenticate(user=user)

        # when : 리뷰 목록 조회 API 호출 & 정렬 조건 추가
        response = api_client.get(self.url, {"is_my_review":True, "ordering": "performance__name"})

        # then : 리뷰 작성 순으로 정렬
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3
        assert response.json()[0]["performance"]["name"] == "베토벤 교향곡"


@pytest.mark.django_db
class TestReviewDetail:

    def test_other_user_review_detail(self, api_client, review_data):
        """다른 유저 리뷰 상세 조회 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user3')
        api_client.force_authenticate(user=user)

        # when : 리뷰 상세 조회 API 호출
        url = reverse('review-detail', args=[review_data["review4"].id])
        response = api_client.get(url)

        # then : 리뷰 상세 반환
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["performance"]["name"] == "베토벤 교향곡"
        assert response.json()["content"] == "재밌어요4"


    def test_update_other_user_review(self, api_client, review_data):
        """다른 유저 리뷰 업데이트 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user3')
        api_client.force_authenticate(user=user)

        # when : 리뷰 수정 API 호출
        url = reverse('review-detail', args=[review_data["review4"].id])
        response = api_client.put(url, {"content":"진짜 재밌어요4"})

        # then : 작성자 외 리뷰 수정 금지 반환
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "이 리뷰를 수정할 권한이 없습니다. 작성자만 수정 할 수 있습니다."

    def test_update_other_user_review(self, api_client, review_data):
        """다른 유저 리뷰 업데이트 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user1')
        api_client.force_authenticate(user=user)

        # when : 리뷰 수정 API 호출
        url = reverse('review-detail', args=[review_data["review4"].id])
        response = api_client.put(url, {"content":"진짜 재밌어요4"})

        # then : 리뷰 수정 성공
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["content"] != "재밌어요4"            # 기존 리뷰 내용
        assert response.json()["content"] == "진짜 재밌어요4"         # 수정한 리뷰 내용

    def test_create_review(self, api_client, performance_data, review_data):
        """리뷰 작성 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user4')
        api_client.force_authenticate(user=user)

        performance_id = performance_data["performance2"].id

        # when : 리뷰 작성 API 호출
        url = reverse('review-list')
        response = api_client.post(url, {"performance":performance_id,"content":"너무 즐거웠어요"})

        # then : 리뷰 생성 성공
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["content"] == "너무 즐거웠어요"

    def test_destroy_review(self, api_client, performance_data, review_data):
        """리뷰 삭제 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user4')
        api_client.force_authenticate(user=user)

        performance_id = performance_data["performance2"].id

        # given : 리뷰 작성 및 생성된 리뷰 조회
        list_url = reverse('review-list')
        create_response = api_client.post(list_url, {"performance":performance_id,"content":"너무 즐거웠어요"})
        list_response = api_client.get(list_url, {"is_my_review":True})

        assert create_response.status_code == status.HTTP_201_CREATED
        assert len(list_response.json()) == 1

        # when : 리뷰 삭제 API 호출
        detail_url = reverse('review-detail', args=[list_response.json()[0]["id"]])
        destroy_response = api_client.delete(detail_url)
        destroy_after_list_response = api_client.get(list_url, {"is_my_review":True})

        # then : 리뷰 삭제
        assert destroy_response.status_code == status.HTTP_204_NO_CONTENT
        assert len(destroy_after_list_response.json()) == 0


@pytest.mark.django_db
class TestReviewReport:

    def setup_method(self, method):
        self.url = reverse('review-report')

    def test_create_review_report(self, api_client, review_data):
        """리뷰 신고 테스트"""

        # given : 유저 토큰 세팅(db 저장된 user_data 활용)
        user = User.objects.get(username='user4')
        api_client.force_authenticate(user=user)

        review_id = review_data["review7"].id

        # when : 리뷰 신고 API 호출
        response = api_client.post(self.url, {"review":review_id, "reason":"spam"})

        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_review_report(self, api_client, review_data, review_report_data):
        """중복 리뷰 신고 테스트"""

        # given: 유저 로그인
        user = User.objects.get(username='user1')
        api_client.force_authenticate(user=user)

        review_id = review_data["review7"].id

        # when: 중복 신고 시도
        response = api_client.post(self.url, {"review": review_id, "reason": "spam"})

        # then: 중복 신고는 400 오류
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['detail'] == ['이미 신고한 리뷰입니다.']

    def test_my_reviews_exclude_reported_reviews(self, api_client, review_data, review_report_data):
        """신고 누적 5회 리뷰 제외 내가 작성한 리뷰 조회 테스트: 마이페이지"""

        # given: 유저 로그인
        user = User.objects.get(username='user3')
        api_client.force_authenticate(user=user)

        # when : 내가 작성한 리뷰 조회 API 호출
        my_review_url = reverse('review-list')
        response = api_client.get(my_review_url, {"is_my_review":True})

        # then : 신고 누적 5회 제외 1건 조회
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_content_of_reported_review(self, api_client, performance_data, review_data, review_report_data):
        """신고 누적 5회 리뷰 컨텐츠 테스트"""

        # given: 유저 로그인
        user = User.objects.get(username='user5')
        api_client.force_authenticate(user=user)

        # when : 공연 리뷰 목록 조회 API 호출
        performance_id = performance_data["performance3"].id
        performance_review_url = reverse('review-list')
        response = api_client.get(performance_review_url, {"performance_id":performance_id})

        # then : 5회 신고된 리뷰 컨텐츠 제한
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3
        assert response.json()[0]["content"] == "신고된 리뷰입니다"
