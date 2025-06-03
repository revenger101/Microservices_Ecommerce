from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re

class User(models.Model):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            MinLengthValidator(3, message="Username must be at least 3 characters long"),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Username can only contain letters, numbers, and underscores"
            )
        ]
    )
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['username', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def clean(self):
        """Custom validation"""
        super().clean()

        # Validate email domain
        if self.email:
            domain = self.email.split('@')[1] if '@' in self.email else ''
            blocked_domains = ['tempmail.com', '10minutemail.com']
            if domain in blocked_domains:
                raise ValidationError({'email': 'Email domain is not allowed'})

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs.get('update_fields', []):
            self.password = make_password(self.password)
        self.full_clean()
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        db_index=True
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
            ('N', 'Prefer not to say')
        ],
        blank=True
    )
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

class UserAddress(models.Model):
    ADDRESS_TYPES = [
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
        ('both', 'Both'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        db_index=True
    )
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='shipping')
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_addresses'
        indexes = [
            models.Index(fields=['user', 'address_type']),
            models.Index(fields=['user', 'is_default']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'address_type'],
                condition=models.Q(is_default=True),
                name='unique_default_address_per_type'
            )
        ]

    def clean(self):
        """Ensure only one default address per type per user"""
        if self.is_default:
            existing_default = UserAddress.objects.filter(
                user=self.user,
                address_type=self.address_type,
                is_default=True
            ).exclude(pk=self.pk)

            if existing_default.exists():
                raise ValidationError('User can only have one default address per type')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)