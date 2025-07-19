from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
import pytz
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from OAhuf_app.models import OutletCart


india_tz = pytz.timezone("Asia/Kolkata")


class CustomUser(AbstractUser):
    # Add any custom fields here
    customer_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    userId = models.CharField(max_length=100, unique=True, blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        self.updated_ist = now_ist
        
        if not self.pk:  # Object is being created
            if self.created_ist is None:
                self.created_ist = now_ist

            super().save(*args, **kwargs)  # First save to get the ID

            if not self.customer_id:
                self.customer_id = f"cust_0{self.id}"
                super().save(update_fields=['customer_id'])
        else:
            self.updated_ist = now_ist
            super().save(*args, **kwargs)
            
            
            
class UserDetails(models.Model):
    currentUser = models.OneToOneField(CustomUser , on_delete=models.CASCADE , related_name='user_details')
    userName = models.CharField(max_length=100)
    userCity = models.CharField(max_length=100)
    userState = models.CharField(max_length=100)
    userCountry = models.CharField(max_length=100)
    userlatitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    userlongitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    userpostalCode = models.CharField(max_length=50, blank=True)
    userLoginIp = models.GenericIPAddressField(null=True, blank=True)
    userVerified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True )
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.userName}"


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=True,blank=True)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state_or_region = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)  # optional: for default shipping/billing

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}, {self.street_address}, {self.city}, {self.country}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    imageUrl =  models.CharField(max_length=255, blank=True)
    careated_at = models.DateTimeField(auto_now_add=True )
    
    created_ist = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    imageUrl =  models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discounted_price =models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items',null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='menu_items',null=True, blank=True)
    avg_reviews = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)

    def has_plate_options(self):
        return self.plate_options.exists()

    @property
    def calculated_discount(self):
        if self.price and self.discounted_price:
            return round((self.price - self.discounted_price) / self.price * 100, 2)
        return 0

    def __str__(self):
        return self.name
        
class PlateOption(models.Model):
  

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='plate_options')
    plate_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def calculated_discount(self):
        if self.price and self.discounted_price:
            return round((self.price - self.discounted_price) / self.price * 100, 2)
        return 0
        

    def __str__(self): 
        return f"{self.menu_item.name} - {self.plate_type.capitalize()}"    
        

## ========================================== Combo Model ======================================


class ComboCategory(models.Model):
    name = models.CharField(max_length=100)
    imageUrl = models.CharField(max_length=255, blank=True)
    for_catering = models.BooleanField(default=False, help_text="Is this combo Category used in catering?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ComboMenu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    imageUrl = models.CharField(max_length=255, blank=True)

    category = models.ForeignKey(ComboCategory, on_delete=models.CASCADE, related_name='combo_menus')
    menu_items = models.ManyToManyField(MenuItem, related_name='combo_menus')
    for_catering = models.BooleanField(default=False, help_text="Is this combo available for catering? Make sure its category also in catering.")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    avg_reviews = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)
        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist
        self.updated_ist = now_ist
        super().save(*args, **kwargs)

    @property
    def calculated_discount(self):
        if self.price and self.discounted_price:
            return round((self.price - self.discounted_price) / self.price * 100, 2)
        return 0

    def __str__(self):
        return self.name



    
class Offer(models.Model):
    OFFER_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('bogo', 'Buy One Get One'),
        ('free_shipping', 'Free Shipping'),
        ('custom', 'Custom'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default='percentage')
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="e.g., 10 for 10% or $10")

    code = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Optional coupon code")
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    usage_limit = models.IntegerField(blank=True, null=True, help_text="Max times this offer can be used")
    per_user_limit = models.IntegerField(blank=True, null=True, help_text="Max usage per user")

    applicable_to = models.CharField(
        max_length=20,
        choices=[
            ('all', 'All Items'),
            ('category', 'Specific Category'),
            ('menu_item', 'Specific Menu Item'),
            ('user', 'Specific User(s)'),
        ],
        default='all'
    )

    categories = models.ManyToManyField('Category', blank=True)
    menu_items = models.ManyToManyField('MenuItem', blank=True)
    users = models.ManyToManyField('CustomUser', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)


    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.title} ({self.offer_type})"

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    is_active = models.BooleanField(default=True)  # You can deactivate carts after checkout
    applied_offer = models.ForeignKey('Offer', null=True, blank=True, on_delete=models.SET_NULL)
    is_party_catering = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def subtotal(self):
        total = 0
        for item in self.items.all():
            if item.plate_option:
                price = item.plate_option.price
            else:
                price = item.item.price or 0
            total += price * item.quantity
        return total

    def discounted_total(self):
        total = 0
        for item in self.items.all():
            if item.plate_option:
                price = item.plate_option.discounted_price or item.plate_option.price
            else:
                price = item.item.discounted_price or item.item.price or 0
            total += price * item.quantity
        return total

    def discount_amount(self):
        if not self.applied_offer or not self.applied_offer.is_valid():
            return 0.0

        offer = self.applied_offer
        subtotal = self.subtotal()

        # Minimum order check
        if offer.min_order_amount and subtotal < offer.min_order_amount:
            return 0.0

        # User-eligibility
        if offer.applicable_to == 'user' and self.user not in offer.users.all():
            return 0.0

        # Category-eligibility
        if offer.applicable_to == 'category':
            if not offer.categories.filter(
                id__in=[ci.item.category_id for ci in self.items.all() if isinstance(ci.item, MenuItem) and ci.item.category_id]
            ).exists():
                return 0.0

        # Menu item eligibility
        if offer.applicable_to == 'menu_item':
            if not offer.menu_items.filter(
                id__in=[ci.item.id for ci in self.items.all() if isinstance(ci.item, MenuItem)]
            ).exists():
                return 0.0

        # Build applicable items
        if offer.applicable_to == 'category':
            applicable_items = [
                item for item in self.items.all()
                if isinstance(item.item, MenuItem) and item.item.category in offer.categories.all()
            ]
        elif offer.applicable_to == 'menu_item':
            applicable_items = [
                item for item in self.items.all()
                if isinstance(item.item, MenuItem) and item.item in offer.menu_items.all()
            ]
        else:
            applicable_items = self.items.all()

        discount = 0.0

        # Discount calculation
        if offer.offer_type == 'percentage':
            discount = (subtotal * offer.value) / 100

        elif offer.offer_type == 'fixed':
            discount = offer.value

        elif offer.offer_type == 'bogo':
            for cart_item in applicable_items:
                qty = cart_item.quantity
                if cart_item.plate_option:
                    unit_price = float(cart_item.plate_option.discounted_price or cart_item.plate_option.price)
                else:
                    unit_price = float(cart_item.item.discounted_price or cart_item.item.price or 0)

                free_qty = qty // 2
                discount += free_qty * unit_price

        if offer.max_discount_amount:
            discount = min(discount, offer.max_discount_amount)

        return discount

    def total(self):
        return max(float(self.discounted_total()) - float(self.discount_amount()), 0)

    
    

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    # menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    
    
    # Generic relation to MenuItem or ComboMenuItem
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE ,null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('content_type', 'object_id')
    
    quantity = models.PositiveIntegerField(default=1)
    plate_option = models.ForeignKey(PlateOption, on_delete=models.SET_NULL, null=True, blank=True)

    plate_option = models.ForeignKey(PlateOption, null=True, blank=True, on_delete=models.SET_NULL)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)

    def clean(self):
        if self.content_type.model_class() not in [MenuItem, ComboMenu]:
            raise ValidationError("Invalid item type for cart.")
            
    class Meta:
        unique_together = ('cart', 'content_type', 'object_id', 'plate_option')  # Prevent duplicate items in the same cart

    def __str__(self):
        return f"{self.item.name} (x{self.quantity}) in Cart #{self.cart.id}"




class OrderSchedule(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='schedule')
    occasion = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)  # optional field

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)
        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist
        self.updated_ist = now_ist
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.occasion} on {self.scheduled_date} at {self.scheduled_time} for Cart #{self.cart.id}"






#payment
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    order_id = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, null=True, blank=True,verbose_name="Cashfree Transaction ID")
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_currency = models.CharField(max_length=10, default='INR')
    customer_id = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    cart_id = models.CharField(max_length=100, null=True, blank=True)
    address_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.order_id} - {self.status}"
    


class WebhookLog(models.Model):
    trxn_id = models.CharField(max_length=1000 , blank=True , null=True)
    order_amount = models.FloatField( blank=True ,null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    payload = models.JSONField()
    status_at_receive = models.CharField(max_length=50, blank=True, null=True)
    status_time = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        if not self.pk and self.created_ist is None:
            self.created_ist = now_ist

        self.updated_ist = now_ist

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Webhook - {self.order_id} at {self.timestamp}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('PREPARING', 'Preparing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    ]
    ahuf_order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    order_id = models.CharField(max_length=100, unique=True)  
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_currency = models.CharField(max_length=10, default='INR')
    customer_id = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    outlet_cart = models.ForeignKey("OAhuf_app.OutletCart", null=True, blank=True, on_delete=models.SET_NULL)
    cart_id = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)         
    address_id = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)       
    status = models.CharField(max_length=50, default='PENDING')  
    order_status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='IN_PROGRESS')
    payment_mode = models.CharField(max_length=50, blank=True, null=True)   
    payment_time = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  
    return_url = models.URLField(blank=True, null=True)
    notify_url = models.URLField(blank=True, null=True)
    order_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_ist = models.DateTimeField(null=True, blank=True)
    updated_ist = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        now_ist = datetime.now(india_tz).replace(tzinfo=None)

        self.updated_ist = now_ist

        if not self.pk:  # Object is being created
            if self.created_ist is None:
                self.created_ist = now_ist

            super().save(*args, **kwargs)

            if not self.ahuf_order_id:
                self.ahuf_order_id = f"AHUF_{str(self.id).zfill(8)}"
                super().save(update_fields=['ahuf_order_id'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"
