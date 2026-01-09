from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product # Ajuste conforme o nome do seu app de produtos

class CartItemSerializer(serializers.ModelSerializer):
    # Definimos os nomes dos campos que o React espera receber
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    # O SerializerMethodField procura uma função chamada get_<nome_do_campo>
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image', 'quantity', 'subtotal']

    # ESTA FUNÇÃO DEVE ESTAR INDENTADA DENTRO DA CLASSE CartItemSerializer
    def get_product_image(self, obj):
        # Lógica para lidar com dict (na criação) ou instância (na listagem)
        if isinstance(obj, dict):
            product = obj.get('product')
        else:
            product = obj.product

        if product:
            # Tenta pegar a imagem principal
            main_img = product.images.filter(main=True).first()
            if main_img:
                return main_img.image.url
            
            # Se não tiver, pega a primeira
            first_img = product.images.first()
            if first_img:
                return first_img.image.url
                
        return None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_cart_price']