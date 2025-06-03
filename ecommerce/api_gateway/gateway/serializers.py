from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import re

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=None, message="Username already exists"),
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=None, message="Email already exists"),
        ]
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    first_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    is_active = serializers.BooleanField(default=True)
    is_verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_username(self, value):
        """Validate username format"""
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores")
        return value

    def validate_email(self, value):
        """Validate email domain"""
        domain = value.split('@')[1] if '@' in value else ''
        blocked_domains = ['tempmail.com', '10minutemail.com']
        if domain in blocked_domains:
            raise serializers.ValidationError("Email domain is not allowed")
        return value

    def validate_phone(self, value):
        """Validate phone number format"""
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return value

class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer not to say')],
        required=False,
        allow_blank=True
    )
    timezone = serializers.CharField(max_length=50, default='UTC')
    language = serializers.CharField(max_length=10, default='en')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class UserAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    address_type = serializers.ChoiceField(
        choices=[('shipping', 'Shipping'), ('billing', 'Billing'), ('both', 'Both')],
        default='shipping'
    )
    street_address = serializers.CharField(max_length=255)
    apartment = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)
    is_default = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    product_sku = serializers.CharField(max_length=100, required=False, allow_blank=True)
    quantity = serializers.IntegerField(min_value=1, max_value=1000)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    product_details = serializers.JSONField(required=False, default=dict)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_number = serializers.CharField(max_length=50, read_only=True)
    user_id = serializers.IntegerField()
    status = serializers.ChoiceField(
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('PROCESSING', 'Processing'),
            ('SHIPPED', 'Shipped'),
            ('DELIVERED', 'Delivered'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
            ('REFUNDED', 'Refunded'),
        ],
        default='PENDING'
    )
    payment_status = serializers.ChoiceField(
        choices=[
            ('PENDING', 'Pending'),
            ('PAID', 'Paid'),
            ('FAILED', 'Failed'),
            ('REFUNDED', 'Refunded'),
        ],
        default='PENDING'
    )

    # Pricing
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    tax_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    # Addresses
    shipping_address = serializers.JSONField(required=False, allow_null=True)
    billing_address = serializers.JSONField(required=False, allow_null=True)

    # Items
    items = OrderItemSerializer(many=True, read_only=True)

    # Metadata
    notes = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    shipped_at = serializers.DateTimeField(read_only=True, allow_null=True)
    delivered_at = serializers.DateTimeField(read_only=True, allow_null=True)

class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)
    shipping_address = serializers.JSONField(required=False, allow_null=True)
    billing_address = serializers.JSONField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, value):
        """Validate order items"""
        if not value:
            raise serializers.ValidationError("Order must have at least one item")

        if len(value) > 50:
            raise serializers.ValidationError("Order cannot have more than 50 items")

        # Check for duplicate products
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products in order")

        return value

class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('PROCESSING', 'Processing'),
            ('SHIPPED', 'Shipped'),
            ('DELIVERED', 'Delivered'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
            ('REFUNDED', 'Refunded'),
        ]
    )
    reason = serializers.CharField(required=False, allow_blank=True)

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs