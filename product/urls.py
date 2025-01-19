from django.urls import path
from .views import ProductListView,ProductCreateView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create', ProductCreateView.as_view(), name='create-product-list'),

]
