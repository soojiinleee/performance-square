from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class BasePaginationResponseMixin:
    """공통 페이지네이션 응답 처리를 위한 Mixin"""

    def get_paginated_response(self, data):
        response = Response(data)

        if self.get_next_link():
            response.headers['Next-Page'] = self.get_next_link()
        if self.get_previous_link():
            response.headers['Previous-Page'] = self.get_previous_link()

        # 전체 데이터 개수 추가 (PageNumberPagination만 적용)
        if hasattr(self, 'page') and hasattr(self.page, 'paginator'):
            response.headers['Total-Count'] = self.page.paginator.count

        return response

class StandardResultsSetPagination(BasePaginationResponseMixin, PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class StandardCursorPagination(BasePaginationResponseMixin, CursorPagination):
    page_size = 10
    ordering = '-created_at'
