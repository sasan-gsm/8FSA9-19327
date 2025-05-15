from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from typing import Dict, Any, List


class CustomPaginationWithCount(PageNumberPagination):
    """
    Custom pagination class includes count information in the response.

    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: List[Dict[str, Any]]) -> Response:
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
