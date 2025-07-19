# Create your views here.
# Booking List + Create
from .models import *
from Ahuf_app.models import *
from .serializers import *
from Ahuf_app.serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render , get_object_or_404,redirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .utils import generate_pdf_bill


class TableListCreateAPIView(APIView):
    def get(self, request):
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Table Status Update (booked/available)
class TableStatusAPIView(APIView):
    def post(self, request, pk):
        table = get_object_or_404(Table, pk=pk)
        status_value = request.data.get("status")
        if status_value in ["available", "booked"]:
            table.status = status_value
            table.save()
            return Response({"status": f"Table marked as {status_value}"})
        return Response({"error": "Invalid status"}, status=400)
 


class BookingListCreateAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Booking created",
                "booking_id": serializer.data['id'],
                "data": serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)
    

class AddToCartAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get("booking_id")
        menu_item_id = request.data.get("menu_item_id")
        plate_option_id = request.data.get("plate_option_id")
        quantity = request.data.get("quantity")

        # Validate required fields (plate_option_id can be None)
        # if not all([booking_id, menu_item_id, quantity]):
        #     return Response({
        #         "success": False,
        #         "message": "booking_id, menu_item_id, and quantity are required."
        #     }, status=status.HTTP_400_BAD_REQUEST)
        if booking_id is None or menu_item_id is None or quantity is None:
            return Response({
                "success": False,
                "message": "booking_id, menu_item_id, and quantity are required."
           }, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id=booking_id)
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except Booking.DoesNotExist:
            return Response({"success": False, "message": "Booking not found."}, status=404)
        except MenuItem.DoesNotExist:
            return Response({"success": False, "message": "Menu item not found."}, status=404)

        quantity = int(quantity)

        # Handle optional plate_option
        plate_option = None
        if plate_option_id:
            try:
                plate_option = PlateOption.objects.get(id=plate_option_id, menu_item=menu_item)
                unit_price = plate_option.discounted_price or plate_option.price
            except PlateOption.DoesNotExist:
                return Response({"success": False, "message": "Plate option not found for this menu item."}, status=404)
        else:
            # No plate_option — use MenuItem price
            unit_price = menu_item.discounted_price or menu_item.price

        # If quantity is 0, remove item from cart
        filter_kwargs = {
            "booking": booking,
            "menu_item": menu_item,
            "plate_option": plate_option
        }

        if quantity == 0:
            deleted_count, _ = OutletCart.objects.filter(**filter_kwargs).delete()
            return Response({
                "success": True,
                "message": "Item removed from cart." if deleted_count else "Item not found in cart."
            }, status=200)

        # Add or update cart item
        cart_item, created = OutletCart.objects.get_or_create(
            **filter_kwargs,
            defaults={
                "quantity": quantity,
                "price": unit_price  
            }
        )

        if not created:
            cart_item.quantity = quantity
            cart_item.price = unit_price 
            cart_item.save()

        return Response({
            "success": True,
            "message": "Item added to cart" if created else "Item updated in cart",
            "data": {
                "menu_item": menu_item.name,
                "plate_type": plate_option.plate_type if plate_option else "N/A",
                "quantity": cart_item.quantity,
                "price": str(cart_item.price),
                "booking_id": booking.id,
            }
        }, status=200)
    



class CartDetailAPIView(APIView):
    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"success": False, "message": "Booking not found"}, status=404)

        cart_items = OutletCart.objects.filter(booking=booking)
        serializer = OutletCartSerializer(cart_items, many=True)

        total_price = sum(item.quantity * item.price for item in cart_items)

        return Response({
            "success": True,
            "booking_id": booking.id,
            "cart_items": serializer.data,
            "total_price": total_price,
            "payment_status": "Paid" if booking.payment else "Unpaid"
            # "data":serializer.data
        }, status=200)



class UpdateCartItemAPIView(APIView):
    def patch(self, request):
        booking_id = request.data.get("booking_id")
        menu_item_id = request.data.get("menu_item_id")
        quantity = request.data.get("quantity")
        plate_size = request.data.get("plate_size", "full")
        if not (booking_id and menu_item_id and quantity):
            return Response({"success": False, "message": "Missing fields"}, status=400)

        try:
            cart_item = OutletCart.objects.get(booking_id=booking_id, menu_item_id=menu_item_id,plate_size=plate_size )
        except OutletCart.DoesNotExist:
            return Response({"success": False, "message": "Cart item not found"}, status=404)

        cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({"success": True, "message": "Cart item updated", "quantity": cart_item.quantity})

class DeleteCartItemAPIView(APIView):
    def delete(self, request):
        booking_id = request.data.get("booking_id")
        menu_item_id = request.data.get("menu_item_id")

        if not booking_id or not menu_item_id:
            return Response({"success": False, "message": "Missing booking_id or menu_item_id"}, status=400)

        deleted_count, _ = OutletCart.objects.filter(
            booking_id=booking_id,
            menu_item_id=menu_item_id
        ).delete()

        if deleted_count == 0:
            return Response({"success": False, "message": "Cart item not found"}, status=404)

        return Response({"success": True, "message": "Item(s) removed from cart"})

class ConfirmBookingAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')

        try:
            booking = Booking.objects.get(id=booking_id, is_confirmed=False)
        except Booking.DoesNotExist:
            return Response({"success": False, "message": "Booking not found"}, status=404)

        cart_items = OutletCart.objects.filter(booking=booking, is_active=True)
        if not cart_items.exists():
            return Response({"success": False, "message": "Cart is empty"}, status=400)

        if not booking.is_takeaway:
            if not booking.table:
                return Response({"success": False, "message": "Table not selected"}, status=400)
            if booking.table.status == 'booked':
                return Response({"success": False, "message": "Table already booked"}, status=400)
            booking.table.status = 'booked'
            booking.table.save()

        booking.is_confirmed = True
        booking.save()
        total_price = sum(item.quantity * item.price for item in cart_items)

        return Response({
            "success": True,
            "message": "Booking confirmed",
            "booking_id": booking.id,
            "total_price": total_price 
        })


#--------------------fetch menuitem-------------------------------------------
class getmenudata(APIView):
    def get(self,request):
        menu_id=request.query_params.get('menu_id')
        menu_data = MenuItem.objects.filter(id=menu_id)
        serializer= MenuItemWithQuantityupdated(menu_data,many=True)

        return Response({"success":True,
                         "message":"Menu fetched successfully",
                         "menu_data":serializer.data
                         },status=200)

#========================payment======================================

class PaymentAndGenerateBillAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        payment_method = request.data.get('payment_method')  # cash, online, barcode

        if payment_method not in ['cash', 'online', 'barcode']:
            return Response({"success": False, "message": "Invalid payment method"}, status=400)

        try:
            booking = Booking.objects.get(id=booking_id, is_confirmed=True , payment = False )
        except Booking.DoesNotExist:
            return Response({"success": False, "message": "Booking not found or not confirmed or payment already done."}, status=404)

        # cart_items = OutletCart.objects.filter(booking=booking)
        cart_items=OutletCart.objects.filter(booking=booking, is_active=True)
        if not cart_items.exists():
            return Response({"success": False, "message": "Cart is empty"}, status=400)

        total_price = sum(item.quantity * item.price for item in cart_items)

        # Create or update bill
        bill, created = Bill.objects.get_or_create(
            booking=booking,
            defaults={'total_amount': total_price, 'payment_method': payment_method}
        )

        if not created:
            bill.total_amount = total_price
            bill.payment_method = payment_method
            bill.save()
        # ✅ Mark booking as paid — FIXED here
        booking.payment = True
        booking.save()

        # ✅ Create order
        ahuf_order_id = f"OAHUF_{str(booking.id).zfill(8)}"
        cust_id = f"cust_{booking.id}"
        Order.objects.create(
                ahuf_order_id = ahuf_order_id ,
                order_id = booking.id,
                order_amount = total_price,
               
                customer_id = cust_id,
                customer_phone = booking.mobile_no,
                outlet_cart  =  cart_items.first() , #     int(payment.cart_id),
                
                status = "DELIVERED",
                payment_mode =  payment_method ,
                payment_time = datetime.now().isoformat(),
              
                return_url = 'https://ahufcafe.com/',
                notify_url = 'https://ahufcafe.com/'
            )

        # Reset table status
        if booking.table:
            booking.table.status = 'available'
            booking.table.save()

        # Generate PDF and save to bill
        pdf_buffer = generate_pdf_bill(booking, cart_items, total_price)
        filename = f"bill_{booking_id}.pdf"
        bill.pdf_file.save(filename, ContentFile(pdf_buffer.getvalue()))
        bill.save()

        # Mark cart items as inactive
        cart_items.update(is_active=False)

        # Send PDF as response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


#=================bill pdf=====================================================================

class BillDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            bill = Bill.objects.get(booking_id=pk)
        except Bill.DoesNotExist:
            return Response({'detail': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




#=====================recentorders==========================

class RecentUnpaidOrdersAPIView(APIView):
    def get(self, request):
        unpaid_orders = Booking.objects.filter(
            is_confirmed=True,
            payment=False
        ).order_by('-booking_time')

        serializer = RecentBookingSerializer(unpaid_orders, many=True)
        return Response({
            "success": True,
            "message": "Unpaid recent bookings fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
