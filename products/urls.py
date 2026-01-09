from django.urls import path
from .api import CategoryListAPIView, ProductListAPIView

urlpatterns = [
    path("category/", CategoryListAPIView.as_view(), name="category-list"),
    path("products/", ProductListAPIView.as_view(), name="products-list"),
]