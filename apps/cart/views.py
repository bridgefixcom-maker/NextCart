from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from apps.products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@method_decorator(login_required, name='dispatch')
class CartView(View):

    def get(self, request):
        cart = get_or_create_cart(request.user)
        items = cart.items.select_related('product').prefetch_related('product__images')
        return render(request, 'cart/cart.html', {
            'cart': cart,
            'items': items,
        })


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_available=True)
        cart = get_or_create_cart(request.user)

        if not product.in_stock:
            return JsonResponse({'success': False, 'message': 'Product out of stock'}, status=400)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if item.quantity < product.stock_quantity:
                item.quantity += 1
                item.save()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f'{product.name} cart mein add ho gaya!',
        })


@method_decorator(login_required, name='dispatch')
class UpdateCartView(View):

    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            item.delete()
        elif quantity <= item.product.stock_quantity:
            item.quantity = quantity
            item.save()

        cart = item.cart if quantity >= 1 else get_or_create_cart(request.user)
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'item_subtotal': str(item.subtotal) if quantity >= 1 else '0',
            'cart_total': str(cart.total_price),
        })


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):

    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = item.cart
        item.delete()
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_total': str(cart.total_price),
        })
