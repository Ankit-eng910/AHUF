
#-------------------------------Table Booking System-----------------------------------------------------

# models.py
# from Ahuf_app.models import *
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
import uuid
class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True,default=None)

    TABLE_STATUS = (
        ('available', 'Available'),
        ('booked', 'Booked'),
    )
    status = models.CharField(max_length=10, choices=TABLE_STATUS, default='available')

    def __str__(self):
        return f"Table {self.table_number} ({self.status})"



class Booking(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{10,15}$')],
        null=True,
        blank=True
    )
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)
    is_takeaway = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.mobile_no:
            self.mobile_no = str(uuid.uuid4())[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{'Takeaway' if self.is_takeaway else 'Dine-in'} | {self.name or 'Guest'}"






#######----------------add to cart-----------------------------------------------------
class OutletCart(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    menu_item = models.ForeignKey('Ahuf_app.MenuItem', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    plate_option = models.ForeignKey('Ahuf_app.PlateOption', null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    added_on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"
 


#=============================bill============================================================
class Bill(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('online', 'Online'),
        ('barcode', 'Barcode'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='bills/', null=True, blank=True) 
    def __str__(self):
        return f"Bill #{self.id} - ₹{self.total_amount}"
    



    
