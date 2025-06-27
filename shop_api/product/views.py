from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductReviewSerializer, CategoryWithCountSerializer, CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer



class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.create(name=serializer.validated_data['name'])
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            category.name = serializer.validated_data['name']
            category.save()
            return Response(CategorySerializer(category).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                product = Product.objects.create(
                    title=serializer.validated_data['title'],
                    description=serializer.validated_data.get('description', ''),
                    price=serializer.validated_data['price'],
                    category_id=serializer.validated_data['category_id']
                )
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            product.title = serializer.validated_data['title']
            product.description = serializer.validated_data.get('description', '')
            product.price = serializer.validated_data['price']
            product.category_id = serializer.validated_data['category_id']
            product.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                review = Review.objects.create(
                    text=serializer.validated_data['text'],
                    product_id=serializer.validated_data['product_id'],
                    stars=serializer.validated_data['stars']
                )
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(APIView):
    def get(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response({'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response({'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():
            review.text = serializer.validated_data['text']
            review.product_id = serializer.validated_data['product_id']
            review.stars = serializer.validated_data['stars']
            review.save()
            return Response(ReviewSerializer(review).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response({'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryWithCountAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryWithCountSerializer(categories, many=True)
        return Response(serializer.data)


class ProductWithReviewsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductReviewSerializer(products, many=True)
        return Response(serializer.data)
