from rest_framework import serializers
from .models import *
from Ahuf_app.models import Order

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class OutletCartSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_image = serializers.SerializerMethodField()
    plate_type = serializers.SerializerMethodField()
    class Meta:
        model = OutletCart
        fields = ['id', 'booking', 'menu_item', 'menu_item_name','menu_item_image', 'quantity', 'price', 'plate_type']

    def get_menu_item_image(self, obj):
        request = self.context.get('request')
        if request and obj.menu_item and obj.menu_item.imageUrl:
            return request.build_absolute_uri(obj.menu_item.imageUrl)
        elif obj.menu_item and obj.menu_item.imageUrl:
            return obj.menu_item.imageUrl.url
        return None
    

    def get_plate_type(self, obj):
        return obj.plate_option.plate_type if obj.plate_option else None


#==================================-bill========================================================================
class BillSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()
    class Meta:
        model = Bill
        fields = ['id', 'booking', 'total_amount',  'generated_at', 'pdf_url', 'cart_items']

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            return request.build_absolute_uri(obj.pdf_file.url)
        return None
    
    def get_cart_items(self, obj):
        cart_items = OutletCart.objects.filter(booking=obj.booking)
        # return OutletCartSerializer(cart_items, many=True).data
        return OutletCartSerializer(cart_items, many=True, context=self.context).data
    
#==============================recent orders================================================
class RecentBookingSerializer(serializers.ModelSerializer):
    table_id= serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()


    class Meta:
        model = Booking
        fields = ['id', 'name', 'mobile_no', 'booking_time', 'table_id', 'is_takeaway','payment','payment_status','total_amount']

    def get_table_id(self, obj):
        return obj.table.id if obj.table else None

    def get_payment_status(self, obj):
        return "Paid" if obj.payment else "Unpaid"
    
    def get_total_amount(self, obj):
        cart_items = OutletCart.objects.filter(booking=obj, is_active=True)
        return sum(item.quantity * item.price for item in cart_items)
    



class OrderWithOutletCartItemsSerializer(serializers.ModelSerializer):
    booking_id = serializers.SerializerMethodField()
    booking_cart_items = serializers.SerializerMethodField()
    is_takeaway = serializers.SerializerMethodField()
    table_id = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'ahuf_order_id',
            'order_id',
            'order_amount',
            'order_currency',
            'customer_id',
            'customer_phone',
            'status',
            'order_status',
            'payment_mode',
            'payment_time',
            'transaction_id',
            'created_at',
            'updated_at',
            'booking_id',
            'is_takeaway', 
            'table_id',         # Custom field: from outlet_cart.booking.id
            'booking_cart_items'    # Custom field: all OutletCart items with same booking
        ]

    def get_booking_id(self, obj):
        if obj.outlet_cart and obj.outlet_cart.booking:
            return obj.outlet_cart.booking.id
        return None
    
    def get_is_takeaway(self, obj):
        if obj.outlet_cart and obj.outlet_cart.booking:
            return obj.outlet_cart.booking.is_takeaway
        return None
    
    def get_table_id(self, obj):
        booking = getattr(obj.outlet_cart, 'booking', None)
        if booking and not booking.is_takeaway and booking.table:
            return booking.table.id
        return None
    
    def get_booking_cart_items(self, obj):
        if obj.outlet_cart and obj.outlet_cart.booking:
            booking_id = obj.outlet_cart.booking.id
            outlet_carts = OutletCart.objects.filter(booking_id=booking_id)
            return OutletCartSerializer(outlet_carts, many=True, context=self.context).data
        return []
