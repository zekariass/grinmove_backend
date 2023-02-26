from rest_framework.pagination import PageNumberPagination
from systems.models import SystemParameter


def get_page_size():
    try:
        page_size_instance = SystemParameter.objects.get(name="PUBLIC_LISTING_PAGE_SIZE")
        page_size = page_size_instance.value
    except:
        page_size = 0
    print("PAGE_SIZE YOOOO ",page_size)
    return page_size


class PublicListingPagination(PageNumberPagination):
    def __init__(self):
        super().__init__()
        # self.pages = int(get_page_size())
        self.page_size = int(get_page_size())



def get_featured_page_size():
    try:
        page_size_instance = SystemParameter.objects.get(name="FEATURED_LISTING_PAGE_SIZE")
        page_size = page_size_instance.value
    except:
        page_size = 0
    # print("PAGE_SIZE YOOOO ",page_size)
    return page_size

class FeaturedListingPagination(PageNumberPagination):
    def __init__(self):
        super().__init__()
        self.page_size = int(get_featured_page_size())
        
    