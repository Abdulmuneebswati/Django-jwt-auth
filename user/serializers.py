from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from product.serializers import ProductSerializer
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # Add the related products

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'dob', 'created_at', 'updated_at', 'products']

class UserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'dob', 'password', 'created_at', 'updated_at','products']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally remove the 'products' field from the response
        if self.context.get('exclude_products', False):
            representation.pop('products', None)

        return representation




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
            },
        }
