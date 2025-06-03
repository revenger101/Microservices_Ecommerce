from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    user_id = models.IntegerField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    # Pricing
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # Addresses
    shipping_address = models.JSONField(null=True, blank=True)
    billing_address = models.JSONField(null=True, blank=True)

    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['payment_status']),
        ]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        self.calculate_totals()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Generate unique order number"""
        import datetime
        now = datetime.datetime.now()
        return f"ORD-{now.strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

    def calculate_totals(self):
        """Calculate order totals from items"""
        items = self.items.all()
        self.subtotal = sum(item.total_price for item in items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_amount - self.discount_amount

    def clean(self):
        """Custom validation"""
        if self.total_amount < 0:
            raise ValidationError('Total amount cannot be negative')

        if self.status == 'DELIVERED' and not self.delivered_at:
            raise ValidationError('Delivered orders must have a delivery date')

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        db_index=True
    )
    product_id = models.IntegerField(db_index=True)
    product_name = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Quantity must be at least 1"),
            MaxValueValidator(1000, message="Quantity cannot exceed 1000")
        ]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message="Price must be positive")]
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    # Product details at time of order
    product_details = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'
        indexes = [
            models.Index(fields=['order', 'product_id']),
            models.Index(fields=['product_id']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product_id'],
                name='unique_product_per_order'
            )
        ]

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Update order totals
        self.order.calculate_totals()
        self.order.save(update_fields=['subtotal', 'total_amount'])

    def clean(self):
        """Custom validation"""
        if self.quantity <= 0:
            raise ValidationError('Quantity must be positive')
        if self.unit_price <= 0:
            raise ValidationError('Unit price must be positive')

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='status_history',
        on_delete=models.CASCADE,
        db_index=True
    )
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True)
    changed_by = models.IntegerField(null=True, blank=True)  # user_id who made the change
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_status_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order.order_number}: {self.from_status} → {self.to_status}"

class OrderPayment(models.Model):
    PAYMENT_METHODS = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CASH_ON_DELIVERY', 'Cash on Delivery'),
    ]

    order = models.ForeignKey(
        Order,
        related_name='payments',
        on_delete=models.CASCADE,
        db_index=True
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True, db_index=True)
    status = models.CharField(max_length=20, default='PENDING')
    gateway_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'order_payments'
        indexes = [
            models.Index(fields=['order', 'status']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id} for Order {self.order.order_number}"