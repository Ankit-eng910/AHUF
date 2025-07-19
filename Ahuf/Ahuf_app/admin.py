# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import *
import os
import uuid
from django.conf import settings


# admin.site.register(CustomUser, UserAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'userId', 'is_staff']
    search_fields = ['username', 'email', 'userId']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'imageUrl', 'careated_at']
#     search_fields = ['name']

class CategoryAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Category
        fields = ['name', 'image']  # image is a virtual field for upload

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image')

        if image_file:
            folder_prefix = f"{instance.name[:3]}{uuid.uuid4().hex[:5]}"
            relative_path = f"static/client_image/{folder_prefix}/"
            upload_dir = os.path.join(settings.BASE_DIR, relative_path)
            os.makedirs(upload_dir, exist_ok=True)

            file_extension = image_file.name.split('.')[-1]
            new_filename = f"{uuid.uuid4().hex[:12]}.{file_extension}"
            file_path = os.path.join(upload_dir, new_filename)

            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            image_url = f"/{relative_path}{new_filename}"
            instance.imageUrl = image_url

        if commit:
            instance.save()

        return instance

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['name', 'imageUrl']

    # def image_tag(self, obj):
    #     if obj.imageUrl:
    #         return f'<img src="{obj.imageUrl}" width="80" height="50" style="object-fit:cover" />'
    #     return "-"
    # image_tag.allow_tags = True
    # image_tag.short_description = "Image"

admin.site.register(Category, CategoryAdmin)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'category__name']

class MenuItemAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'discounted_price', 'category', 'subcategory', 
                  'avg_reviews', 'total_reviews', 'is_active', 'image', 'imageUrl']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process image if provided
        image_file = self.cleaned_data.get('image')
        if image_file:
            name = self.cleaned_data.get('name', 'img')
            
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
            instance.imageUrl = image_url
        
        if commit:
            instance.save()
        return instance

from django.contrib import admin
from django import forms
from .models import MenuItem, PlateOption

# Inline admin for PlateOption
class PlateOptionInline(admin.TabularInline):
    model = PlateOption
    extra = 1
    min_num = 0
    verbose_name = "Plate Type Option"
    verbose_name_plural = "Plate Type Options"

# Custom form to add toggle
class MenuItemAdminForm(forms.ModelForm):
    use_plate_type = forms.BooleanField(
        required=False,
        label="Use plate type pricing (Half/Full)",
        help_text="Check this if this item uses separate pricing for half/full plate.",
    )

    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['use_plate_type'].initial = self.instance.has_plate_options()

# Admin for MenuItem
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm
    inlines = [PlateOptionInline]
    list_display = ['name', 'price', 'discounted_price', 'calculated_discount', 'subcategory', 'avg_reviews', 'category', 'total_reviews', 'is_active', 'crated_at']
    list_filter = ['subcategory', 'is_active']
    search_fields = ['name', 'subcategory__name']
    readonly_fields = ['calculated_discount', 'imageUrl']

    fieldsets = (
        (None, {
            'fields': (
                'name', 'description', 'imageUrl', 'price', 'discounted_price',
                'category', 'subcategory', 'avg_reviews', 'total_reviews', 'is_active', 'use_plate_type'
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Optional: if use_plate_type is checked, clear direct price fields (you can keep this or not)
        if form.cleaned_data.get('use_plate_type'):
            obj.price = None
            obj.discounted_price = None
            obj.save()



## ===================================== Combo ADMIN =========================================

class ComboCategoryAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = ComboCategory
        fields = ['name', 'imageUrl', 'image' , 'for_catering']

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image')
        if image_file:
            folder_prefix = f"combo_cat_{uuid.uuid4().hex[:5]}"
            relative_path = f"static/ComboCategory_images/{folder_prefix}/"
            upload_dir = os.path.join(settings.BASE_DIR, relative_path)
            os.makedirs(upload_dir, exist_ok=True)

            file_extension = image_file.name.split('.')[-1]
            new_filename = f"{uuid.uuid4().hex[:12]}.{file_extension}"
            file_path = os.path.join(upload_dir, new_filename)

            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            instance.imageUrl = f"/{relative_path}{new_filename}"

        if commit:
            instance.save()
        return instance



class ComboMenuAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = ComboMenu
        fields = ['name', 'description', "for_catering", 'category', 'menu_items', 'price', 'discounted_price', 'avg_reviews' , 'total_reviews', 'is_active', 'imageUrl', 'image']

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image')
        if image_file:
            folder_prefix = f"combo_menu_{uuid.uuid4().hex[:5]}"
            relative_path = f"static/ComboMenu_images/{folder_prefix}/"
            upload_dir = os.path.join(settings.BASE_DIR, relative_path)
            os.makedirs(upload_dir, exist_ok=True)

            file_extension = image_file.name.split('.')[-1]
            new_filename = f"{uuid.uuid4().hex[:12]}.{file_extension}"
            file_path = os.path.join(upload_dir, new_filename)

            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            instance.imageUrl = f"/{relative_path}{new_filename}"

        if commit:
            instance.save()
            self.save_m2m()
        return instance



@admin.register(ComboCategory)
class ComboCategoryAdmin(admin.ModelAdmin):
    form = ComboCategoryAdminForm
    list_display = ['name']


@admin.register(ComboMenu)
class ComboMenuAdmin(admin.ModelAdmin):
    form = ComboMenuAdminForm
    list_display = ['name', 'category', 'price', 'discounted_price', 'is_active']
    filter_horizontal = ['menu_items']





@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'offer_type',
        'code',
        'value',
        'start_date',
        'end_date',
        'is_active',
    )
    list_filter = (
        'offer_type',
        'is_active',
        'start_date',
        'end_date',
    )
    search_fields = (
        'title',
        'code',
        'description',
    )
    filter_horizontal = (
        'categories',
        'menu_items',
        'users',
    )
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'offer_type',
                'value',
                'code',
                'is_active',
            )
        }),
        ('Validity', {
            'fields': (
                'start_date',
                'end_date',
            )
        }),
        ('Restrictions', {
            'fields': (
                'min_order_amount',
                'max_discount_amount',
                'usage_limit',
                'per_user_limit',
            )
        }),
        ('Applicability', {
            'fields': (
                'applicable_to',
                'categories',
                'menu_items',
                'users',
            )
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_date'


#payment
from .models import Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        # 'customer_email',
        'order_amount',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('order_id',  'customer_id')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('trxn_id','order_amount','order_id', 'status_at_receive','status_time', 'timestamp')
    search_fields = ('order_id', 'status_at_receive')
    list_filter = ('status_at_receive', 'timestamp')
    readonly_fields = ('timestamp', 'order_id', 'payload', 'status_at_receive')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id', 'customer_phone', 'order_amount', 'status',
        'payment_mode', 'payment_time', 'order_status', 'created_at'
    )
    list_filter = ('status', 'order_status', 'payment_mode', 'created_at')
    search_fields = ('order_id', 'customer_id', 'customer_phone', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


