from django.urls import path
from .views import ProductListView,ProductCreateView,ProductDetailView,ProductUpdateView,ProductDeleteView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create', ProductCreateView.as_view(), name='create-product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:id>/edit/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product-update'),
]
