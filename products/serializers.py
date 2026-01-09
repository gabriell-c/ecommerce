from rest_framework import serializers
from .models import Category, Product, ProductImage

# 1. Criamos um serializer para as imagens primeiro
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "main"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    # 2. Chamamos o serializer de imagem aqui dentro. 
    # O nome da variável deve ser o mesmo do 'related_name' no models.py (images)
    images = ProductImageSerializer(many=True, read_only=True)
    
    # Opcional: Se quiser trazer o nome da categoria em vez de apenas o ID
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        # 3. Adicionamos "images" na lista de campos
        fields = [
            "id", 
            "name", 
            "slug", 
            "description", 
            "price", 
            "stock", 
            "category", 
            "category_name", 
            "images"
        ]