from django.db import models
from django.conf import settings
from apps.products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cod',    'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2)

    # Delivery address
    full_name      = models.CharField(max_length=150)
    phone          = models.CharField(max_length=15)
    address_line1  = models.CharField(max_length=255)
    address_line2  = models.CharField(max_length=255, blank=True)
    city           = models.CharField(max_length=100)
    state          = models.CharField(max_length=100)
    pincode        = models.CharField(max_length=10)

    # Payment
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='cod')
    is_paid        = models.BooleanField(default=False)

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.user.email}'


class OrderItem(models.Model):
    order        = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')

    # Price snapshot at time of purchase
    product_name = models.CharField(max_length=255)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    quantity     = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_items'

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity}x {self.product_name}'
