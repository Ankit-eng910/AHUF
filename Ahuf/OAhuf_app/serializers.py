from rest_framework import serializers
from .models import *

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
    plate_type = serializers.SerializerMethodField()
    class Meta:
        model = OutletCart
        fields = ['id', 'booking', 'menu_item', 'menu_item_name', 'quantity', 'price', 'plate_type']

    def get_plate_type(self, obj):
        return obj.plate_option.plate_type if obj.plate_option else None


########### ------------------bill-------------------------
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
        cart_items = OutletCart.objects.filter(booking=obj.booking, is_active=True)
        return OutletCartSerializer(cart_items, many=True).data

#==============================recent orders========================
class RecentBookingSerializer(serializers.ModelSerializer):
    table_id= serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'name', 'mobile_no', 'booking_time', 'table_id', 'is_takeaway','payment','payment_status']

    def get_table_id(self, obj):
        return obj.table.id if obj.table else None

    def get_payment_status(self, obj):
        return "Paid" if obj.payment else "Unpaid"
