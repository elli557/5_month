"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.app_settings import swagger_settings
from product.views import (
    CategoryListAPIView,
    CategoryDetailAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ReviewListAPIView,
    ReviewDetailAPIView,
    CategoryWithCountAPIView,
    ProductWithReviewsAPIView,
)
from . import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/categories/', CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetailAPIView.as_view()),
    path('api/v1/products/', ProductListAPIView.as_view()),
    path('api/v1/products/<int:id>/', ProductDetailAPIView.as_view()),
    path('api/v1/reviews/', ReviewListAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetailAPIView.as_view()),
    path('api/v1/categories_with_count/', CategoryWithCountAPIView.as_view()),
    path('api/v1/products_with_reviews/', ProductWithReviewsAPIView.as_view()),
]
urlpatterns += swagger.urlpatterns