from datetime import date, timedelta

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status

from core.schemas import PAGINATION_PARAMS
from .models import PerformanceStatus
from .serializers import PerformanceSerializer

PERFORMANCE_LIST_SCHEMA = extend_schema(
    tags=["공연"],
    summary="공연 목록 조회",
    description="""
        - 공연 장르 별 목록 조회
        - 공연 상태 별 목록 조회
    """,
    parameters=[
        OpenApiParameter(
            name="genre_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="공연 장르 id",
            required=False,
        ),
        OpenApiParameter(
            name="status",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            enum=[e.value for e in PerformanceStatus],
            description="공연 상태",
            required=False,
            examples=[
                OpenApiExample("공연 예정", value="upcoming"),
                OpenApiExample("공연 중", value="ongoing"),
                OpenApiExample("공연 종료", value="ended"),
            ],
        ),
    ]
    + PAGINATION_PARAMS,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=PerformanceSerializer(many=True),
            description="공연 목록 리스트",
        )
    },
    examples=[
        OpenApiExample(
            response_only=True,
            summary="로그인 안 한 유저",
            name="unauthorized",
            value=[
                {
                    "id": 1,
                    "genre": {"id": 6, "name": "대중음악"},
                    "name": "유명 가수 콘서트1",
                    "status": "upcoming",
                    "price": 150000,
                    "started_at": date.today() + timedelta(days=5),
                    "ended_at": date.today() + timedelta(days=10),
                    "like_count": 5,
                    "is_liked": False,
                }
            ],
        ),
        OpenApiExample(
            response_only=True,
            name="authorized",
            summary="로그인 유저",
            description="좋아요(is_liked) 확인",
            value=[
                {
                    "id": 1,
                    "genre": {"id": 6, "name": "대중음악"},
                    "name": "유명 가수 콘서트1",
                    "status": "upcoming",
                    "price": 150000,
                    "started_at": date.today() + timedelta(days=5),
                    "ended_at": date.today() + timedelta(days=10),
                    "like_count": 5,
                    "is_liked": True,
                },
                {
                    "id": 2,
                    "genre": {"id": 9, "name": "뮤지컬"},
                    "name": "유명 뮤지컬1",
                    "status": "upcoming",
                    "price": 170000,
                    "started_at": date.today() + timedelta(days=100),
                    "ended_at": date.today() + timedelta(days=365),
                    "like_count": 250,
                    "is_liked": False,
                },
            ],
        ),
    ],
)

PERFORMANCE_RETRIEVE_SCHEMA = extend_schema(
    tags=["공연"],
    summary="공연 상세 조회",
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="공연 id",
            required=True,
            examples=[OpenApiExample("공연 id", value="6")],
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=PerformanceSerializer(),
            description="공연 상세",
        )
    },
    examples=[
        OpenApiExample(
            response_only=True,
            summary="로그인 안 한 유저",
            name="unauthorized",
            value={
                "id": 1,
                "genre": {"id": 6, "name": "대중음악"},
                "name": "유명 가수 콘서트1",
                "status": "upcoming",
                "price": 150000,
                "started_at": date.today() + timedelta(days=5),
                "ended_at": date.today() + timedelta(days=10),
                "like_count": 5,
                "is_liked": False,
            },
        ),
        OpenApiExample(
            response_only=True,
            name="liked performance by authorized",
            summary="로그인 유저 - 공연에 좋아요 o",
            description="is_liked 필드 확인",
            value={
                "id": 1,
                "genre": {"id": 6, "name": "대중음악"},
                "name": "유명 가수 콘서트1",
                "status": "upcoming",
                "price": 150000,
                "started_at": date.today() + timedelta(days=5),
                "ended_at": date.today() + timedelta(days=10),
                "like_count": 5,
                "is_liked": True,
            },
        ),
        OpenApiExample(
            response_only=True,
            name="just performance by authorized",
            summary="로그인 유저 - 공연에 좋아요 x",
            description="is_liked 필드 확인",
            value={
                "id": 2,
                "genre": {"id": 9, "name": "뮤지컬"},
                "name": "유명 뮤지컬1",
                "status": "upcoming",
                "price": 170000,
                "started_at": date.today() + timedelta(days=100),
                "ended_at": date.today() + timedelta(days=365),
                "like_count": 250,
                "is_liked": False,
            },
        ),
    ],
)

PERFORMANCE_LIKE_CREATE_SCHEMA = extend_schema(
    tags=["공연"],
    summary="공연 좋아요 등록/취소",
    description="""
        ✅ 로그인 필수
        ✅ is_liked 값의 상태에 따라 요청 후 결과 달라짐
            - is_liked == True 호출 시 -> 좋아요 취소
            - is_liked == False 호출 시 -> 좋아요 등록
    """,
    parameters=[
        OpenApiParameter(
            name="performance_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="공연 id",
            required=True,
            examples=[OpenApiExample("공연 id", value="6")],
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=PerformanceSerializer(),
            description="is_liked 업데이트",
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=status.HTTP_401_UNAUTHORIZED,
            description="로그인 정보 없는 경우 401 에러",
        ),
    },
    examples=[
        OpenApiExample(
            response_only=True,
            summary="로그인 안 한 유저",
            name="unauthorized",
            status_codes=[status.HTTP_401_UNAUTHORIZED],
            value={"detail": "Authentication credentials were not provided."},
        ),
        OpenApiExample(
            response_only=True,
            name="liked performance by authorized",
            summary="로그인 유저 - 좋아요한 공연",
            description="is_liked 필드 확인",
            status_codes=[status.HTTP_201_CREATED],
            value={
                "id": 6,
                "genre": {"id": 6, "name": "대중음악"},
                "name": "유명 가수 콘서트1",
                "status": "upcoming",
                "price": 150000,
                "started_at": date.today() + timedelta(days=5),
                "ended_at": date.today() + timedelta(days=10),
                "like_count": 5,
                "is_liked": False,
            },
        ),
        OpenApiExample(
            response_only=True,
            name="just performance by authorized",
            summary="로그인 유저 - 좋아요 안 한 공연",
            description="is_liked 필드 확인",
            status_codes=[status.HTTP_201_CREATED],
            value={
                "id": 6,
                "genre": {"id": 6, "name": "대중음악"},
                "name": "유명 가수 콘서트1",
                "status": "upcoming",
                "price": 150000,
                "started_at": date.today() + timedelta(days=5),
                "ended_at": date.today() + timedelta(days=10),
                "like_count": 5,
                "is_liked": True,
            },
        ),
    ],
)

LIKED_PERFORMANCE_LIST_SCHEMA = extend_schema(
    tags=["마이페이지"],
    summary="좋아요 클릭한 공연 목록 조회",
    description="로그인 필수",
    parameters=PAGINATION_PARAMS,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=PerformanceSerializer(many=True),
            description="좋아요한 공연 목록 리스트",
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=status.HTTP_401_UNAUTHORIZED,
            description="로그인 정보 없는 경우 401 에러",
        ),
    },
    examples=[
        OpenApiExample(
            response_only=True,
            summary="로그인 안 한 유저",
            name="unauthorized",
            status_codes=[status.HTTP_401_UNAUTHORIZED],
            value={"detail": "Authentication credentials were not provided."},
        ),
        OpenApiExample(
            response_only=True,
            name="authorized",
            summary="로그인 유저",
            description="좋아요(is_liked) 확인",
            status_codes=[status.HTTP_200_OK],
            value=[
                {
                    "id": 1,
                    "genre": {"id": 6, "name": "대중음악"},
                    "name": "유명 가수 콘서트1",
                    "status": "upcoming",
                    "price": 150000,
                    "started_at": date.today() + timedelta(days=5),
                    "ended_at": date.today() + timedelta(days=10),
                    "like_count": 5,
                    "is_liked": True,
                },
                {
                    "id": 2,
                    "genre": {"id": 9, "name": "뮤지컬"},
                    "name": "유명 뮤지컬1",
                    "status": "upcoming",
                    "price": 170000,
                    "started_at": date.today() + timedelta(days=100),
                    "ended_at": date.today() + timedelta(days=365),
                    "like_count": 250,
                    "is_liked": True,
                },
            ],
        ),
    ],
)
