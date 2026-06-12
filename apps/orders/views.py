from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from apps.cart.models import Cart, CartItem
from .models import Order, OrderItem


def get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):

    def get(self, request):
        cart = get_cart(request.user)
        items = cart.items.select_related('product')

        if not items.exists():
            return redirect('cart:cart')

        return render(request, 'orders/checkout.html', {
            'cart': cart,
            'items': items,
            'user': request.user,
        })

    def post(self, request):
        cart = get_cart(request.user)
        items = cart.items.select_related('product')

        if not items.exists():
            return redirect('cart:cart')

        # Collect form data
        full_name     = request.POST.get('full_name', '').strip()
        phone         = request.POST.get('phone', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        city          = request.POST.get('city', '').strip()
        state         = request.POST.get('state', '').strip()
        pincode       = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')

        # Basic validation
        if not all([full_name, phone, address_line1, city, state, pincode]):
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'items': items,
                'user': request.user,
                'error': 'Saari fields fill karo.',
                'form_data': request.POST,
            })

        # Create Order
        order = Order.objects.create(
            user           = request.user,
            total_amount   = cart.total_price,
            full_name      = full_name,
            phone          = phone,
            address_line1  = address_line1,
            address_line2  = address_line2,
            city           = city,
            state          = state,
            pincode        = pincode,
            payment_method = payment_method,
        )

        # Create OrderItems from CartItems
        for item in items:
            OrderItem.objects.create(
                order        = order,
                product      = item.product,
                product_name = item.product.name,
                price        = item.product.effective_price,
                quantity     = item.quantity,
            )

        # Clear cart
        items.delete()

        return redirect('orders:order_detail', order_id=order.id)


@method_decorator(login_required, name='dispatch')
class OrderDetailView(View):

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'orders/order_detail.html', {'order': order})


@method_decorator(login_required, name='dispatch')
class OrderHistoryView(View):

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
        return render(request, 'orders/order_history.html', {'orders': orders})
