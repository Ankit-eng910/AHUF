
#--------------------------table booking-------------------------------

from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id','table_number', 'status']
    list_filter = ['status']
    search_fields = ['table_number']

@admin.register(OutletCart)
class OutletCartAdmin(admin.ModelAdmin):
    list_display = ('booking', 'menu_item', 'quantity', 'price', 'added_on')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'mobile_no', 'booking_time', 'is_takeaway']
    list_filter = ['is_takeaway']
    search_fields = ['name']
    


class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'total_amount', 'payment_method', 'generated_at', 'pdf_link']

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html(f'<a href="{obj.pdf_file.url}" target="_blank">View PDF</a>')
        return "-"
    pdf_link.short_description = "PDF File"

admin.site.register(Bill, BillAdmin)
