from app.models.schemas.util import PageParam, PageResponse


def translate_query_pagination(
    query_param: PageParam, total: int
) -> tuple[int, int, PageResponse]:
    """
    returns limit: int and offset: int and paging: ResponsePagination
    with pagesize undesided
    """
    limit = query_param.size or total
    offset = (query_param.page - 1) * limit if query_param.page else 0
    current_page = query_param.page or 1

    total_pages = -(-total // query_param.size) if query_param.size else 1

    paging = PageResponse(
        total=total,
        total_pages=total_pages,
        page=current_page,
        size=max(0, min((total - offset), limit)),
    )
    return limit, offset, paging
