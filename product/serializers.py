from rest_framework import serializers
from .models import Product
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField() 

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'owner', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at','id']

    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "username": obj.owner.username,
            "email": obj.owner.email,
            "name": obj.owner.name,
        }