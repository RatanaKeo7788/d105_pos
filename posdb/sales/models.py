# sales/models.py

from django.db import models
from django.contrib.auth.models import User 


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food',        'Food & Drink'),
        ('electronics', 'Electronics'),
        ('clothing',    'Clothing'),
        ('household',   'Household'),
        ('other',       'Other'),
    ]

    name      = models.CharField(max_length=255)
    category  = models.CharField(max_length=100, blank=True)
    barcode   = models.CharField(max_length=100, blank=True)
    price     = models.DecimalField(max_digits=10, decimal_places=2)
    stock     = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image     = models.ImageField(upload_to='products/', blank=True, null=True)  # ✅ add this

    def __str__(self):
        return f"{self.name}  —  ${self.price}  (stock: {self.stock})"
        return f"{self.name} — ${self.price:.2f}"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    STATUS_CHOICES = [
        ('open',      'Open'),
        ('paid',      'Paid'),
        ('refunded',  'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    # Replace 'cashier = models.CharField(...)' with a ForeignKey:
    cashier    = models.ForeignKey(
                    User,
                    on_delete=models.SET_NULL,   # keep the order if the staff account is deleted
                    null=True,
                    related_name='orders',
                 )
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    notes      = models.TextField(blank=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        name = self.cashier.username if self.cashier else 'unknown'
        return f"Order #{self.pk}  [{self.status.upper()}]  by {name}  —  ${self.total:.2f}"

    #class Meta:
    #    ordering = ['-created_at']

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product   = models.ForeignKey(Product, on_delete=models.PROTECT)   # PROTECT prevents deleting a product that has sales
    quantity  = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)   # price at time of sale

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}  @  ${self.unit_price}"