from rest_framework.pagination import PageNumberPagination


class Page(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    # 定制传参
    page_size_query_param = 'size'
    # 最大一页的数据
    max_page_size = 40
