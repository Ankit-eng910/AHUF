from rest_framework import serializers
from .models import *
import os ,uuid
from django.conf import settings
from datetime import datetime, timedelta
from pytz import timezone





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'imageUrl']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'



class CategoryWithSubSerializer(serializers.ModelSerializer):
    subcount = serializers.SerializerMethodField()
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'imageUrl', 'subcount', 'subcategories']

    def get_subcount(self, obj):
        return obj.subcategories.count()



class MenuItemSerializer(serializers.ModelSerializer):
    # calculated_discount = serializers.ReadOnlyField()
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = MenuItem
        fields = [
            'id','name', 'description', 'price', 'discounted_price', 'category', 'subcategory',
            'avg_reviews', 'total_reviews', 'imageUrl', 'image',"calculated_discount"
        ]
        read_only_fields = ['imageUrl',"calculated_discount"]

    def create(self, validated_data):
        image_file = validated_data.pop('image')
        name = validated_data.get('name', 'img')

        # Custom folder logic
        folder_prefix = f"{name[:3]}{uuid.uuid4().hex[:5]}"
        relative_path = f"static/Menu_images/{folder_prefix}/"
        upload_dir = os.path.join(settings.BASE_DIR, relative_path)
        os.makedirs(upload_dir, exist_ok=True)

        # Generate filename and save image
        file_extension = image_file.name.split('.')[-1]
        new_filename = f"{uuid.uuid4().hex[:12]}.{file_extension}"
        file_path = os.path.join(upload_dir, new_filename)

        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Construct URL and save
        image_url = f"/{relative_path}{new_filename}"
        validated_data['imageUrl'] = image_url

        return MenuItem.objects.create(**validated_data)

class MenuItemWithQuantitySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'imageUrl', 'price', 'discounted_price',
            'category', 'subcategory', 'category_name', 'subcategory_name', 'avg_reviews', 'total_reviews',
            'is_active', 'calculated_discount', 'quantity'
        ]
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None
    

    def get_quantity(self, obj):
        user = self.context.get('user')
        is_party_catering = self.context.get('is_party_catering', False) 

        if user and user.is_authenticated:
            print("I am From Serializer if ")
            cart = Cart.objects.filter(user=user, is_active=True, is_party_catering=is_party_catering).first()
            if cart:
                if is_party_catering:
                    # cart_item = cart.items.filter(menu_item=obj).first()
                    ctype = ContentType.objects.get_for_model(obj)
                    cart_item = cart.items.filter(content_type=ctype, object_id=obj.id).first()
                    return cart_item.quantity if cart_item else 5
                else :
                    ctype = ContentType.objects.get_for_model(obj)
                    cart_item = cart.items.filter(content_type=ctype, object_id=obj.id).first()
                    return cart_item.quantity if cart_item else 0
            else:
                if is_party_catering:
                    return 5
                else:
                    return 0
        else:
            if is_party_catering:
                return 5
            else :
                return 0
        return 0
        
        
        
        
class MenuItemWithQuantityupdated(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    # quantity = serializers.SerializerMethodField()
    pricing = serializers.SerializerMethodField()  # ðŸ‘ˆ dynamic pricing
    has_plate_type = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'imageUrl',
            'category', 'subcategory', 'category_name', 'subcategory_name',
            'avg_reviews', 'total_reviews', 'is_active', 'calculated_discount',
            # 'quantity', 
            'has_plate_type' , 'pricing'
        ]

    def get_has_plate_type(self, obj):
        return obj.has_plate_options()


    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None

    def get_pricing(self, obj):
        user = self.context.get('user')
        is_party_catering = self.context.get('is_party_catering', False)

        cart = None
        if user and user.is_authenticated:
            cart = Cart.objects.filter(user=user, is_active=True, is_party_catering=is_party_catering).first()

        if obj.plate_options.exists():
            result = []
            for option in obj.plate_options.all():
                quantity = 5 if is_party_catering else 0
                if cart:
                    ctype = ContentType.objects.get_for_model(obj)
                    cart_item = cart.items.filter(content_type=ctype, object_id=obj.id, plate_option=option).first()
                    if cart_item:
                        quantity = cart_item.quantity

                result.append({
                    "plate_type_id": option.id,
                    "plate_type": option.plate_type,
                    "price": option.price,
                    "discounted_price": option.discounted_price,
                    "discount_percent": option.calculated_discount(),
                    "quantity": quantity
                })
            return result

        # Base price with no plate options
        quantity = 5 if is_party_catering else 0
        if cart:
            ctype = ContentType.objects.get_for_model(obj)
            cart_item = cart.items.filter(content_type=ctype, object_id=obj.id, plate_option__isnull=True).first()
            if cart_item:
                quantity = cart_item.quantity

        return [{
            "plate_type": None,
            "price": obj.price,
            "discounted_price": obj.discounted_price,
            "discount_percent": round((obj.price - obj.discounted_price) / obj.price * 100, 2)
            if obj.price and obj.discounted_price else 0,
            "quantity": quantity
        }]
        
        
        
        
##  ==================================== Combo Menu ============================================

class ComboCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboCategory
        fields = ['id', 'name', 'imageUrl']


class ComboMenuSerializer(serializers.ModelSerializer):
    # category = ComboCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=ComboCategory.objects.all(), source='category', write_only=True)
    quantity = serializers.SerializerMethodField()
    menu_items = MenuItemSerializer(many=True, read_only=True)
    menu_item_ids = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), many=True, write_only=True, source='menu_items')

    class Meta:
        model = ComboMenu
        fields = [
            'id', 'name', 'description', 'imageUrl',
            'price', 'discounted_price', 'calculated_discount',
            'is_active', 'category', 'category_id' , 'quantity' , 'avg_reviews' ,
            'total_reviews' ,
            'menu_items', 'menu_item_ids'
        ]
    
    def get_quantity(self, obj):
        user = self.context.get('user')
        is_party_catering = self.context.get('is_party_catering', False) 

        if user and user.is_authenticated:
            print("I am From Serializer if ccccccccccccccccccccccccc")
            cart = Cart.objects.filter(user=user, is_active=True, is_party_catering=is_party_catering).first()
            
            if cart:
                print("I got cart")
                if is_party_catering:
                    # cart_item = cart.items.filter(menu_item=obj).first()
                    ctype = ContentType.objects.get_for_model(obj)
                    cart_item = cart.items.filter(content_type=ctype, object_id=obj.id).first()
                    print(cart_item)
                    return cart_item.quantity if cart_item else 5
                else :
                    ctype = ContentType.objects.get_for_model(obj)
                    cart_item = cart.items.filter(content_type=ctype, object_id=obj.id).first()
                    print(cart_item)
                    return cart_item.quantity if cart_item else 0
            else:
                print("i didn't get cart")
                if is_party_catering:
                    return 5
                else:
                    return 0
        else:
            if is_party_catering:
                return 5
            else :
                return 0

    

## CART SERIALIZER

# from rest_framework import serializers
# from .models import Cart, CartItem, MenuItem

class CartItemSerializer(serializers.ModelSerializer):
    menu_item_details = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    schedule_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'menu_item_details','item_type', 'schedule_details']

    def get_menu_item_details(self, obj):
        item = obj.item
        if not item:
            return {}
        print("DEBUG:", item.name, item.price)
        plate_option = obj.plate_option
        return {
            'id': item.id,
            'name': item.name,
            'price': item.price ,
            'plate_price': plate_option.price if plate_option else None,
            'plate_option_id': plate_option.id if plate_option else None,
            'plate_option': plate_option.plate_type if plate_option else None,
            'quantity': obj.quantity,
            'discounted_price': obj.unit_price ,
            'imageUrl': getattr(item, 'imageUrl', None),
            'avg_reviews': getattr(item, 'avg_reviews', 0),
            'calculated_discount': int(getattr(item, 'calculated_discount', 0))
        }
    def get_item_type(self,obj):
        if obj.content_type:
            model_name = obj.content_type.model
             
            if model_name == 'combomenu':  # Adjust if your model name differs
                
                return 'combo'
        return 'menu'
    def get_schedule_details(self, obj):
        cart = obj.cart
        if cart.is_party_catering and hasattr(cart, 'schedule'):
            schedule = cart.schedule
            return {
                'occasion': schedule.occasion,
                'scheduled_date': schedule.scheduled_date,
                'scheduled_time': schedule.scheduled_time,
                'notes': schedule.notes
            }
        return None
        
        
# ======================================= order Schedule 

india_tz = timezone("Asia/Kolkata")

class OrderScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSchedule
        fields = ['occasion', 'scheduled_date', 'scheduled_time', 'notes']

    def validate(self, data):
        date = data['scheduled_date']
        time = data['scheduled_time']
        schedule_dt = datetime.combine(date, time)
        schedule_dt = india_tz.localize(schedule_dt)

        now = datetime.now(india_tz)
        if schedule_dt < now + timedelta(hours=5):
            raise serializers.ValidationError("Scheduled time must be at least 5 hours from now.")

        return data

class AddOrUpdateCartItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    item_type = serializers.ChoiceField(choices=['menu', 'combo'])  # distinguish models
    plate_option_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=0)
    is_party_catering = serializers.BooleanField()

    def validate(self, attrs):
        item_id = attrs.get('item_id')
        item_type = attrs.get('item_type')
        plate_option_id = attrs.get('plate_option_id')

        # Validate existence of the item based on type
        if item_type == 'menu':
            try:
                menu_item = MenuItem.objects.get(id=item_id)
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError({"item_id": "Menu item does not exist."})

            if plate_option_id:
                if not PlateOption.objects.filter(id=plate_option_id, menu_item=menu_item).exists():
                    raise serializers.ValidationError({"plate_option_id": "Invalid plate option for this menu item."})

        elif item_type == 'combo':
            if plate_option_id:
                raise serializers.ValidationError({"plate_option_id": "Combo menus don't have plate options."})
            if not ComboMenu.objects.filter(id=item_id).exists():
                raise serializers.ValidationError({"item_id": "Combo menu does not exist."})

        return attrs
    
class OfferSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )
    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'description', 'offer_type', 'value', 'code',
            'start_date', 'end_date', 'is_active',
            'min_order_amount', 'max_discount_amount', 'usage_limit', 'per_user_limit',
            'applicable_to', 'categories', 'menu_items', 'users',
        ]


    


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


    def create(self, validated_data):
        user = self.context['request'].user

        # If the new address is marked as default, unset default from all previous ones
        if validated_data.get('is_default', False):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # If is_default is being set to True, remove it from others
        if validated_data.get('is_default', False):
            Address.objects.filter(user=user, is_default=True).exclude(pk=instance.pk).update(is_default=False)

        return super().update(instance, validated_data)
        
        
class CustomerDetailsSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=100)
    # customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)
    cart_id = serializers.IntegerField()
    address_id = serializers.IntegerField()


class CashfreeOrderSerializer(serializers.Serializer):
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_currency = serializers.ChoiceField(choices=[('INR', 'INR')])
    customer_details = CustomerDetailsSerializer()
    
    
    
class OrderSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()
    outlet_cart = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()
    is_party_catering = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'ahuf_order_id',
            'order_id',
            'order_amount',
            'order_currency',
            'customer_id',
            'customer_phone',
            'cart_id',      # Raw FK id
            'cart',         # Full cart detail (optional)
            'outlet_cart',
            'is_party_catering',
            'address_id',   # Raw FK id
            'address',      # Full address detail (optional)
            'status',
            'order_status',
            'payment_mode',
            'payment_time',
            'transaction_id',
            'return_url',
            'notify_url',
            'created_at',
            'updated_at',
            'created_at_formatted', 'updated_at_formatted',
        ]
        read_only_fields = ('created_at', 'updated_at', 'ahuf_order_id','order_id', 'transaction_id')

    def get_cart(self, obj):
        request = self.context.get("request")
        if request and request.query_params.get("include_cart", "").lower() == "true":
            if obj.cart_id:
                cart_items = obj.cart_id.items.all()
                return CartItemSerializer(cart_items, many=True).data
        elif self.context.get("include_cart") == True:
            if obj.cart_id:
                cart_items = obj.cart_id.items.all()
                return CartItemSerializer(cart_items, many=True).data
        return None
    
     

    def get_address(self, obj):
        request = self.context.get("request")
        if request and request.query_params.get("include_address", "").lower() == "true":
            return AddressSerializer(obj.address_id).data if obj.address_id else None
        elif self.context.get("include_address") == True:
            return AddressSerializer(obj.address_id).data if obj.address_id else None
        return None
        
    def get_created_at_formatted(self, obj):
        if obj.created_at:
            return obj.created_at.strftime('%B %d, %Y, %I:%M%p')  # e.g. June 24, 2025, 11:11AM
        return None

    def get_updated_at_formatted(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime('%B %d, %Y, %I:%M%p')  # e.g. June 24, 2025, 11:15AM
        return 
    
    def get_is_party_catering(self, obj):
        if obj.cart_id:
            return obj.cart_id.is_party_catering
        return False
