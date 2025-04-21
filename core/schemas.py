from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


PAGINATION_PARAMS = [
    # request params
    OpenApiParameter(
        name="page",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="페이지 번호",
        required=False,
    ),
    OpenApiParameter(
        name="page_size",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="페이지 당 데이터 개수",
        required=False,
    ),
    # response header
    OpenApiParameter(
        name="Total-Count",
        type=int,
        location=OpenApiParameter.HEADER,
        response=True,
        description="전체 데이터 개수",
    ),
    OpenApiParameter(
        name="Next-Page",
        type=OpenApiTypes.URI,
        location=OpenApiParameter.HEADER,
        response=True,
        description="다음 페이지 URL",
    ),
    OpenApiParameter(
        name="Previous-Page",
        type=OpenApiTypes.URI,
        location=OpenApiParameter.HEADER,
        response=True,
        description="이전 페이지 URL",
    ),
]
