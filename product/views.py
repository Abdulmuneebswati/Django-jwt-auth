from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)

        products = Product.objects.all()
        
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data)
    

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)

            # Serialize the product data
            serializer = ProductSerializer(product)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            # Handle the case where the product is not found
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id)
            if request.user.id != product.owner.id:
                return Response({"detail": "You are not authorized to update this product."}, status=status.HTTP_403_FORBIDDEN)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            # Handle the case where the product is not found
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND) 
        
class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id)
            if request.user.id != product.owner.id:
                return Response({"detail": "You are not authorized to update this product."}, status=status.HTTP_403_FORBIDDEN)
            product.delete()
            return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            # Handle the case where the product is not found
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND) 