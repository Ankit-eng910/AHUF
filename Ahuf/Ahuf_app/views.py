from .models import *
from .serializers import *
import os ,uuid ,json , requests ,hmac ,hashlib ,base64
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render , get_object_or_404
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from urllib.parse import unquote
from django.contrib.auth.models import AnonymousUser
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify
from django.http import HttpResponse



def verifyUser(token):
    url = f"https://user-auth.otpless.app/auth/v1/validate/token"

    payload = json.dumps({
    "token": f"{token}"
    })
    headers = {
    'Content-Type': 'application/json',
    'clientId': config('YOUR_CLIENT_ID'),
    'clientSecret': config('YOUR_CLIENT_SECRET')
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response

    # if "errorCode" in response:
    #     return False
    # elif "token" in response:
    #     return True 
    # else :
    #     return False


def set_token_cookie(response, token):
    response.set_cookie(
        key="backup_access_token",
        value=token,
        max_age=60 * 60 * 24,  # 1 day
        secure=True,
        httponly=False,
        samesite='None',
        path='/',
        domain='.ahufcafe.com'  
    )
    return response


def delete_token_cookie(response):
    response.delete_cookie(
        key="backup_access_token",
        path='/'
    )
    return response




class UserLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response({
                "message": "Token Not Found",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = verifyUser(token)
        if "errorCode" in data:
            return Response(data)
        elif "token" in data:
            pass
        else:
            return Response(data)
        # data = token

        user_id = data.get("userId")
        token = data.get("token")
        phone = data.get("identities", [{}])[0].get("identityValue", "")
        phone = phone[2:] if len(phone)>10 else phone
        ip = data.get("network", {}).get("ip")
        location = data.get("network", {}).get("ipLocation", {})

        # Step 2: Save/Update CustomUser
        # user = CustomUser.objects.get(userId = user_id)
        if CustomUser.objects.filter(userId = user_id).exists():
            user = CustomUser.objects.get(userId = user_id)
            if user.token != token:  
                user.token = token
                user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else :

            user, created = CustomUser.objects.get_or_create(userId=user_id)
            user.token = token
            user.phone_number = phone
            user.username = user.username or f"user_{phone}"  # fallback username
            user.save()

            # Step 3: Use that user to save UserDetails
            user_details, _ = UserDetails.objects.get_or_create(currentUser=user)
            user_details.userName = f"user_{phone[-4:]}"
            user_details.userCity = location.get("city", {}).get("name", "")
            user_details.userState = location.get("subdivisions", {}).get("name", "")
            user_details.userCountry = location.get("country", {}).get("name", "")
            user_details.userpostalCode = location.get("postalCode", "")
            user_details.userlatitude = location.get("latitude")
            user_details.userlongitude = location.get("longitude")
            user_details.userLoginIp = ip
            user_details.userVerified = True
            user_details.save()

        # Optional: Login the user if you want to use Django session auth
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Login and data save successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        


       



# @method_decorator(csrf_exempt, name='dispatch')
class MenuItemAdd(APIView):
    def post(self,request):

        data = request.data.copy()
        serializer =  MenuItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Item Added!",
                    "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {
                    "success": False,
                    "message": "We got some error.",
                    "data": serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

        
## Add Sub Category -----------------------------------------------------------------   

class SubCategoryViewSet(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        category_id = request.data.get('category_id')

        if not name or not category_id:
            return Response({'error': 'name and category_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        subcategory = SubCategory.objects.create(name=name, category=category)
        serializer = SubCategorySerializer(subcategory)  # ← fix is here
        return Response(
            {
                    "success": True,
                    "message": "We Added Your Sub Category.",
                    "data": serializer.data
                    }, status=status.HTTP_201_CREATED)


## Get Sub Category By Category ID-----------------------------------------------------------------

class SubCategoryListView(APIView):
    def get(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({"error": "Missing category_id"}, status=status.HTTP_400_BAD_REQUEST)

        subcategories = SubCategory.objects.filter(category_id=category_id)
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(
            {
                    "success": True,
                    "message": "We got Sub Categories.",
                    "data": serializer.data
                    }, status=status.HTTP_200_OK)



class CategoryViewSet(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        image_file = request.FILES.get('image')

        if not name or not image_file:
            return Response({'error': 'name and image are required.'}, status=status.HTTP_400_BAD_REQUEST)

        folder_prefix = f"{name[:3]}{uuid.uuid4().hex[:5]}"
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

        # Save to DB
        category = Category.objects.create(name=name, imageUrl=image_url)
        serializer = CategorySerializer(category)  # ← fix is here
        return Response(
            {
                    "success": True,
                    "message": "We Added Your Category.",
                    "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
    


class CategoryUpdate(APIView):
    def put(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        
        name = request.data.get('name', category.name)
        if not name:
            name = category.name
        image_file = request.FILES.get('image')

        # If a new image is uploaded
        if image_file:
            old_image_path = os.path.join(settings.BASE_DIR, category.imageUrl.lstrip("/"))

            image_folder = os.path.dirname(old_image_path)
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

            
            file_extension = image_file.name.split('.')[-1]
            new_filename = f"{uuid.uuid4().hex[:12]}.{file_extension}"
            file_path = os.path.join(image_folder, new_filename)

            os.makedirs(image_folder, exist_ok=True)  
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

             
            relative_path = os.path.relpath(file_path, settings.BASE_DIR).replace("\\", "/")
            category.imageUrl = f"/{relative_path}"

        category.name = name
        category.save()

        serializer = CategorySerializer(category)
        return Response(
            {
                    "success": True,
                    "message": "We Updated Your Category.",
                    "data": serializer.data
                    }, status=status.HTTP_200_OK)


# Get 

class GetFilterCategories(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            {
                    "success": True,
                    "message": "We got your Categories.",
                    "data": serializer.data
                    }, status=status.HTTP_200_OK)
    

# Fet Menu Items================================================================================

    
class GetMenuItems(APIView):
    def get(self, request, *args, **kwargs):

        auth = JWTAuthentication()
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is None:
            user = None
        else:
            user, token = user_auth_tuple
        

        category_id = request.query_params.get('categoryId')
        sub_category_id = request.query_params.get('subCategoryId')
        is_party_catering = request.query_params.get('is_party_catering',False)
        
        if is_party_catering == "true":
            is_party_catering = True
        else:
            is_party_catering = False

        menu_items = MenuItem.objects.all()

        if category_id:
            menu_items = menu_items.filter(category=category_id)

        if sub_category_id:
            menu_items = menu_items.filter(subcategory=sub_category_id)

        serializer = MenuItemWithQuantityupdated(menu_items, many=True, context={'user': user,"is_party_catering": is_party_catering})
        return Response( {
                    "success": True,
                    "message": "We got your Menu details.",
                    "data": serializer.data
                    }, status=status.HTTP_200_OK)
    

# Get Recomnded Menu ---------------------------------------------------------


class RecomdatedMenu(APIView):
    def get(self, request, *args, **kwargs):

        # Trying to Get User
        auth = JWTAuthentication()
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is None:
            user = None
        else:
            user, token = user_auth_tuple

        # Geting Item 
        items = MenuItem.objects.all().order_by('-avg_reviews')
        Menuserializer = MenuItemWithQuantitySerializer(items, many=True, context={'user': user})
        items = Menuserializer.data
        top_per_category = {}
        for item in items:
            itemcat = item.get("category")
            if f"{itemcat}" not in top_per_category:
                top_per_category[f"{itemcat}"] = item


        # serializer = MenuItemSerializer(top_per_category, many=True)
        return Response( {
                    "success": True,
                    "message": "We got your Menu details.",
                    "data": top_per_category.values()
                    }, status=status.HTTP_200_OK)


# Search Menu -----------------------------------------------------------------------


class SearchMenu(APIView):
    def get(self, request, *args, **kwargs):

        # Trying to Get User
        auth = JWTAuthentication()
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is None:
            user = None
        else:
            user, token = user_auth_tuple

        search_query = request.query_params.get('search_query', '')
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(subcategory__name__icontains=search_query)
            )
        
        serializer = MenuItemWithQuantitySerializer(menu_items, many=True , context={'user': user})
        return Response( {
                    "success": True,
                    "message": "We got your Menu details.",
                    "data": serializer.data
                    }, status=status.HTTP_200_OK)




# ADD OR UPDATE CART DATA ---------------------------------------------------------------

class RemoveCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = AddOrUpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Invalid data.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        item_id = serializer.validated_data['item_id']
        item_type = serializer.validated_data['item_type']
        quantity = serializer.validated_data['quantity']
        is_party = serializer.validated_data['is_party_catering']
        plate_option_id = serializer.validated_data['plate_option_id']

        if item_type == 'menu':
            model_class = MenuItem
        elif item_type == 'combo':
            model_class = ComboMenu
        else:
            return Response({
                "success": False,
                "message": "Invalid item type. Must be 'menu' or 'combo'."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
             
            item_instance = model_class.objects.get(id=item_id)
        except model_class.DoesNotExist:
            return Response({
                "success": False,
                "message": f"{item_type} item does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            cart = Cart.objects.get(
                user_id=request.user,
                is_active=True,
                is_party_catering=is_party
            )
        except:
            return Response({
                "success":False,
                "message" : "Cart is not present"
            }, status=status.HTTP_404_NOT_FOUND)

        content_type = ContentType.objects.get_for_model(model_class)
        try:
            if plate_option_id != None:
                cart_item = CartItem.objects.get(
                    cart=cart,
                    content_type=content_type,
                    object_id=item_instance.id,
                    plate_option_id = plate_option_id

                )
            else:
                cart_item = CartItem.objects.get(
                    cart=cart,
                    content_type=content_type,
                    object_id=item_instance.id
                )

        except:
            return Response({
                "success":False,
                "message": "Cart item not present."
            }, status=status.HTTP_404_NOT_FOUND)


        # Delete the cart item
        cart_item.delete()

        # If cart is now empty, delete the cart
        if not cart.items.exists():
            cart.delete()
            return Response({
                "success": True,
                "message": "Cart is empty.",
                "data": []
            }, status=status.HTTP_200_OK)

        return Response({
            "success": True,
            "message": "Cart item removed successfully."
        }, status=status.HTTP_200_OK)






class AddOrUpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddOrUpdateCartItemSerializer(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data['item_id']
            item_type = serializer.validated_data['item_type']
            quantity = serializer.validated_data['quantity']
            is_party = serializer.validated_data['is_party_catering']
            plate_option_id = serializer.validated_data.get('plate_option_id')

            # Get model and instance
            if item_type == 'menu':
                model_class = MenuItem
            elif item_type == 'combo':
                model_class = ComboMenu
            else:
                return Response({
                    "success": False,
                    "message": "Invalid item type. Must be 'menu' or 'combo'."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                item_instance = model_class.objects.get(id=item_id)
                if item_type == 'menu' and plate_option_id:
                    plate_option = PlateOption.objects.get(id=plate_option_id, menu_item=item_instance)
                    unit_price = plate_option.discounted_price or plate_option.price
                else:
                    plate_option = None
                    unit_price = item_instance.discounted_price or item_instance.price
            except model_class.DoesNotExist:
                return Response({
                    "success": False,
                    "message": f"{item_type} item does not exist."
                }, status=status.HTTP_404_NOT_FOUND)

            # Enforce minimum quantity for party-catering
            if is_party and quantity > 0 and quantity < 5:
                return Response({
                    "success": False,
                    "message": "Minimum quantity for party catering items is 5."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get or create cart
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                is_active=True,
                is_party_catering=is_party
            )

            # Block if user already has an opposite-type cart
            opposite_cart = Cart.objects.filter(
                user=request.user,
                is_active=True,
                is_party_catering=not is_party
            ).first()

            if opposite_cart and opposite_cart.items.exists():
                return Response({
                    "success": False,
                    "message": "You cannot mix party-catering and regular items in one cart."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get or create the cart item
            content_type = ContentType.objects.get_for_model(model_class)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                content_type=content_type,
                object_id=item_instance.id,
                plate_option=plate_option
            )

            if quantity == 0 and (not cart.is_party_catering):
                cart_item.delete()
                
                # Check if cart is empty after deletion
                if not cart.items.exists():
                    cart.delete()
                    return Response({
                        "success": True,
                        "message": "Cart is empty.",
                        "data": []
                    }, status=status.HTTP_200_OK)

                return Response({
                    "success": True,
                    "message": "Cart item removed successfully."
                }, status=status.HTTP_200_OK)
            elif quantity < 5 and cart.is_party_catering:
                cart_item.delete()
                
                # Check if cart is empty after deletion
                if not cart.items.exists():
                    cart.delete()
                    return Response({
                        "success": True,
                        "message": "Cart is empty.",
                        "data": []
                    }, status=status.HTTP_200_OK)
                return Response({
                    "success": True,
                    "message": "Cart item removed successfully."
                }, status=status.HTTP_200_OK)

            cart_item.quantity = quantity
            
            cart_item.unit_price = unit_price
            cart_item.save()

            return Response({
                "success": True,
                "message": "Cart item added or updated successfully."
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# class AddOrUpdateCartItemView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = AddOrUpdateCartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             menu_item_id = serializer.validated_data['menu_item_id']
#             quantity = serializer.validated_data['quantity']
#             menu_item = MenuItem.objects.get(id=menu_item_id)
            
#             cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
            
#             if quantity == 0:
#                 if cart_item:
#                     cart_item.delete()
#                 return Response({
#                     "success": True,
#                     "message": "Cart item removed successfully."
#                 }, status=status.HTTP_200_OK)

#             cart_item.quantity = quantity
#             cart_item.save()

#             return Response({
#                 "success": True,
#                 "message": "Cart item added or updated successfully."
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "success": False,
#                 "errors": serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)




## GET CART DETAILS -------------------------------------------------------------------------


class GetCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        user = request.user
        if not cart:
            return Response({
                "success": True,
                "message": "Cart is empty.",
                "data": []
            }, status=status.HTTP_200_OK)

        cart_items = cart.items.all()
        serializer = CartItemSerializer(cart_items, many=True)

        discount = float(cart.discount_amount())
        subtotal = float(cart.discounted_total())
        try:
            dis_per = round((discount/subtotal)*100,2)
        except : 
            dis_per = 0.0

        # offer Code already applied
        if cart.applied_offer :
            offer = cart.applied_offer
            return Response({
            "success": True,
            "message": "Cart fetched successfully.",
            "is_party_catering":cart.is_party_catering,
            "data": serializer.data,
            "discount": cart.discount_amount(),
            "subtotal": cart.discounted_total(),
            "discount_percenrage" : dis_per,
            "total_payoff": cart.total(),
            "offer": offer.code,
            "cart_id":cart.id,
            "user_id":user.id,
            "user_number" : user.phone_number
            })
        
        subt = float(cart.subtotal())
        total_pay = float(cart.discounted_total())
        try:
            per_discount = round(((subt-total_pay)/subt)*100,2)
        except:
            per_discount = 0.0
            
        return Response({
            "success": True,
            "message": "Cart fetched successfully.",
            "is_party_catering":cart.is_party_catering,
            "data": serializer.data,
            "subtotal": cart.subtotal(),
            "discount_percenrage" : per_discount,
            "total_payoff": cart.discounted_total(),
            "cart_id":cart.id,
            "user_id":user.id,
            "user_number" : user.phone_number
        }, status=status.HTTP_200_OK)
    # Get cart post method to apply offer
    
    def post(self, request):
        code = request.data.get('code')
        user = request.user
        try:
            cart = Cart.objects.get(user=user, is_active=True)
        except Cart.DoesNotExist:
            return Response({"error": "Active cart not found."}, status=404)

        try:
            offer = Offer.objects.get(code=code)
        except Offer.DoesNotExist:
            return Response({"error": "Invalid offer code."}, status=400)

        if not offer.is_valid():
            return Response({"error": "Offer expired or inactive."}, status=400)

        # Validate against cart (see discount_amount logic)
        cart.applied_offer = offer
        discount = cart.discount_amount()
        if discount == 0:
            cart.applied_offer = None
            return Response({"error": "Offer not applicable to this cart."}, status=400)

        cart.save()
        return Response({
            "success": True,
            "message": "Offer applied successfully.",
            "discount": discount,
            "subtotal": cart.discounted_total(),
            "discount_percenrage" : float((float(discount)/float(cart.discounted_total()))*100),
            "total_payoff": cart.total(),
            "offer": offer.title,
        })












## PAGES RENDER APIS  --------------------------------------------------------------------

class MainHomePageView(APIView):
    def get(self, request, *args, **kwargs):

        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))
        
        trackOrder = False
        if user.is_authenticated:
            if Order.objects.filter(customer_id = "cust_0"+str(user.id), order_active=True).exists():
                trackOrder = True
        

        Category_data = Category.objects.all()
        serializers_data = CategoryWithSubSerializer(Category_data, many=True)
        context = {
            'categories': serializers_data.data,
            'user' : user,
            'trackOrder' : trackOrder
        }
        
        return render(request, 'index.html', context)
    

class BlogPageView(APIView):
    def get(self, request ):
        
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        context = {
            "user": user
        }
        
        
        return render(request , 'blog.html' , context)
    

class AboutPageView(APIView):
    def get(self, request):

        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        context = {
            "user": user
        }

        return render(request, 'about.html' ,context )
    
class LoginPageView(APIView):
    def get(self,request):
        return render(request , 'login.html')
    
class ViewCartPageView(APIView):
    def get(self,request):

        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        context = {
            "user": user ,
            "address_data": serializer.data
        }

        return render(request , 'view-cart.html',context)
    

class MenuDetailsPage(APIView):
    def get(self,request,category,subcategory,item_name):

        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))
            
        try:
            
            trackOrder = False
            if user.is_authenticated:
                if Order.objects.filter(customer_id = "cust_0"+str(user.id), order_active=True).exists():
                    trackOrder = True
            
            item_name = unquote(item_name)
            category = unquote(category)
            subcategory = unquote(subcategory)
            
            
            menudetails = MenuItem.objects.get(
                name=item_name,
                category__name=category,
                subcategory__name=subcategory
            )
            serializer = MenuItemWithQuantityupdated(menudetails, context={'user': user})
            Category_data = Category.objects.all()
            serializers_data = CategoryWithSubSerializer(Category_data, many=True)
        
            context = {
                'categories': serializers_data.data,
                "data": serializer.data,
                'trackOrder' : trackOrder,
                "user": user
            }
        
            return render(request , 'menu-detail.html',context)
        
        except MenuItem.DoesNotExist:
            return render(request, '404-page.html', status=404)
            

def Html404Page(request, exception):
    return render(request, '404-page.html', status=404)
    
    
class TermAndConditions(APIView):
    def get(self,request):
        return render(request , 'terms_and_conditions.html')
    
class RefundPolicy(APIView):
    def get(self , request):
        return render(request , 'refund_policy.html')
        
  


class CodeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        # return Response({"msg":"Working"})
        code_str = request.data.get('code_code')
        cart = Cart.objects.get(user=request.user, is_active=True)
        try:
            code = Offer.objects.get(code=code_str, is_active=True)
        except Offer.DoesNotExist:
            return Response(
                {"error": "Invalid Offer code."},
                status=status.HTTP_400_BAD_REQUEST
            )
        now = timezone.now()
        # 1) Validate time range
        if code.start_date > now or code.end_date < now:
            return Response(
                {"error": "Code is not valid at this time."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # 2) Compute cart total (before any discount)
        cart_total = float(
            sum([item.menu_item.discounted_price * item.quantity for item in cart.items.all()])
        )
        # 3) Validate min order amount
        if cart_total < float(code.min_order_amount):
            return Response(
                {"error": "Cart total does not meet the minimum required for this code."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # 4) Validate per-user usage limit
        if request.user in code.users.all() and code.per_user_limit <= 0:
            return Response(
                {"error": "You have already used this code."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # 5) Figure out which CartItems this code actually applies to
        if code.applicable_to == 'specific':
            applicable_items = cart.items.filter(
                menu_item__in=code.menu_items.all()
            )
        else:  # code.applicable_to == 'all'
            applicable_items = cart.items.all()
        if not applicable_items.exists():
            return Response(
                {"error": "Code not applicable to selected items."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # 6) Calculate discount based on offer_type
        discount = 0.0
        if code.offer_type == 'fixed':
            # A flat discount regardless of cart_total (so long as cart_total ≥ min_order_amount)
            discount = float(code.value)
        elif code.offer_type == 'percentage':
            # A percentage of the full cart_total
            discount = (float(code.value) / 100.0) * cart_total
            if code.max_discount_amount:
                discount = min(discount, float(code.max_discount_amount))
        elif code.offer_type == 'bogo':
            # BUY ONE GET ONE FREE logic:
            # For each CartItem in applicable_items:
            #   free_qty = quantity // 2
            #   discount += free_qty * (menu_item.discounted_price)
            for cart_item in applicable_items:
                qty = cart_item.quantity
                unit_price = float(cart_item.menu_item.discounted_price)
                free_qty = qty // 2
                discount += free_qty * unit_price
            # In a typical BOGO, there's no "max_discount_amount" cap,
            # but if you do want to enforce a maximum, uncomment:
            # if code.max_discount_amount:
            #     discount = min(discount, float(code.max_discount_amount))
        else:
            return Response(
                {"error": "Unsupported offer type."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # 7) Final payable amount
        final_amount = cart_total - discount
        # 8) (Optionally) Register that this user has used the code
        #     so that per_user_limit can be decremented or recorded elsewhere.
        # code.users.add(request.user)
        # code.per_user_limit = code.per_user_limit - 1
        # code.save()
        
        code_title = code.title.strip('"')
        message = f"{code_title} applied successfully!"
        
        return Response({
            "success": True,
            "cart_total": cart_total,
            "discount": round(discount, 2),
            "final_amount": round(final_amount, 2),
            "message": message
        }, status=status.HTTP_200_OK)
    


class OfferAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            offer = get_object_or_404(Offer, pk=pk , is_active = True)
            serializer = OfferSerializer(offer)
            return Response({
                "success": True,
                "message": "Offer retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        offers = Offer.objects.filter(is_active = True)
        serializer = OfferSerializer(offers, many=True)
        return Response({
            "success": True,
            "message": "All offers retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Offer created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Failed to create offer.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Offer updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Failed to update offer.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        offer.delete()
        return Response({
            "success": True,
            "message": "Offer deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
    


class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address_id =  request.query_params.get('id', '')
        if address_id :
            addresses = Address.objects.filter(user=request.user,id = address_id)
        else:
            addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Update address
class AddressUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        serializer = AddressCreateUpdateSerializer(address, data=request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Delete address
class AddressDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.delete()
        return Response({"success": True, "message": "Address deleted."}, status=status.HTTP_204_NO_CONTENT)
        
        

# Payment
from .models import Payment
from decouple import config  # Assuming you're using python-decouple
class paymentpage(APIView):
    def post(self, request):
        
        access_token = request.COOKIES.get('access_token')
        
        try:
            serializer = CashfreeOrderSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            data = serializer.validated_data
            order_id = 'Order' + str(uuid.uuid4())[:8]
            # Save to DB
            Payment.objects.create(
                order_id=order_id,
                order_amount=data['order_amount'],
                order_currency=data['order_currency'],
                customer_id=data['customer_details']['customer_id'],
                cart_id=data['customer_details']['cart_id'],  
                address_id=data['customer_details']['address_id'],
                customer_phone=data['customer_details']['customer_phone'],
                status='PENDING'
            )
            payload = {
                "order_id": order_id,
                "order_amount": float(data['order_amount']),
                "order_currency": data['order_currency'],
                "customer_details": {
                    "customer_id": data['customer_details']['customer_id'],
                    "customer_phone": data['customer_details']['customer_phone'],
                },
                "order_meta": {
                    "return_url": f"https://www.ahufcafe.com/response/?order_id={order_id}"
                },
                "notify_url": "https://www.ahufcafe.com/api/cashfree/webhook/"
            }
            headers = {
                "Content-Type": "application/json",
                "x-api-version": "2022-01-01",
                "x-client-id": config('CASHFREE_CLIENT_ID'),
                "x-client-secret": config('CASHFREE_CLIENT_SECRET')
            }
            response = requests.post(
                f"{settings.CASHFREE_BASE_URL}/orders",
                json=payload,
                headers=headers,
                timeout=10  # optional timeout
            )
            if response.status_code == 200:
                order_data = response.json()
                payment_link = order_data.get('payment_link')
                if request.query_params.get("json") == "true":
                    # return Response({"payment_link": payment_link}, status=status.HTTP_200_OK)
                    api_response = Response({"payment_link": payment_link}, status=status.HTTP_200_OK)
                    set_token_cookie(api_response, access_token)
                    return api_response
                redirect_response = redirect(payment_link)
                set_token_cookie(redirect_response, access_token)
                return redirect_response
            return render(request, '404-page.html', {'message': 'Payment link creation failed'})
        except requests.RequestException as e:
            return Response({"error": "Payment gateway error", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": "Server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import redirect


def payment_response_view(request):
    
    backup_access_token = request.COOKIES.get('backup_access_token')
    
    order_id = request.GET.get('order_id')
    if not order_id:
        return render(request, 'order_confirm.html', {'error': 'Missing order_id in URL.'})
    headers = {
        'x-api-version': config("APIVERSION"),
        "x-client-id": config("CASHFREE_CLIENT_ID"),
        "x-client-secret": config("CASHFREE_CLIENT_SECRET")
    }
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}/payments"
    try:
        response_api = requests.get(url, headers=headers)
        if response_api.status_code == 200:
            data = response_api.json()
            payment_status =  Payment.objects.get(order_id = data[0].get('order_id'))
            payment_status.status = data[0].get('payment_status')
            payment_status.save()
            response = render(request,'order_confirm.html', {'payment_data': data, 'backup_access_token':backup_access_token})
        else:
            response = render(request,'order_confirm.html', {
                'error': 'Failed to fetch payment status.',
                'status_code': response_api.status_code,
                'response_text': response_api.text ,
                'backup_access_token':backup_access_token
            })
    except Exception as e:
        response = render(request, 'order_confirm.html', {
            'error': str(e),
            'backup_access_token': backup_access_token
        })


    delete_token_cookie(response)
    return response









# SECRET_KEY = "ktvwg6cdy2pd8w8ginsw"
# class CashfreeWebhook(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data  # Get webhook data
#         received_signature = request.headers.get("x-webhook-signature")
#         computed_signature = hmac.new(
#             config("WEBHOOK_SECRET_KEY").encode(),
#             json.dumps(data, separators=(",", ":")).encode(),
#             hashlib.sha256
#         ).hexdigest()
#         computed_signature_base64 = base64.b64encode(bytes.fromhex(computed_signature)).decode()
#         print("computed_signature",computed_signature_base64,"\n received_signature",received_signature)
#         if computed_signature_base64 != received_signature:
#             print("error : Invalid signature")
#         event_type = data.get("type")
#         order_id = data.get("data", {}).get("order").get("order_id")
#         order_amount = data.get("data", {}).get("order").get("order_amount")
#         txn_id = data.get("data", {}).get("payment").get("cf_payment_id")
#         timestamp = data.get('event_time')
#         status_changed = data.get("data", {}).get("payment").get('payment_status')
#         if event_type == "PAYMENT_SUCCESS_WEBHOOK":
            
            
#             payment = Payment.objects.get(order_id=order_id)
#             payment.status = "SUCCESS"
#             payment.transaction_id = txn_id
#             payment.save()

#             cart_instance = Cart.objects.get(id=payment.cart_id)
#             cart_instance.is_active = False
#             cart_instance.save()
#             address_instance = Address.objects.get(id = payment.address_id)


#             WebhookLog.objects.create(
#                 trxn_id=txn_id,
#                 order_amount=order_amount,
#                 order_id=order_id,
#                 payload=data,
#                 status_time = timestamp,
#                 status_at_receive=status_changed,
#             )


#             Order.objects.create(
#                 order_id = order_id,
#                 order_amount = order_amount,
#                 order_currency = data.get("data", {}).get("order").get("order_currency"),
#                 customer_id = payment.customer_id,
#                 customer_phone = payment.customer_phone,
#                 cart_id = cart_instance , #     int(payment.cart_id),
#                 address_id =  address_instance , #  int(payment.address_id),
#                 status = status_changed,
#                 payment_mode = data.get("data", {}).get("payment").get("payment_method") ,
#                 payment_time = data.get("data", {}).get("payment").get("payment_time"),
#                 transaction_id = txn_id,
#                 return_url = 'https://ahufcafe.com/',
#                 notify_url = 'https://www.ahufcafe.com/api/cashfree/webhook/'
#             )
            
#             return Response({
#                 "message": "Payment received",
#                 "order_id": order_id }, status=status.HTTP_200_OK)
#         elif event_type == "PAYMENT_FAILED_WEBHOOK":
#             WebhookLog.objects.create(
#                 trxn_id=txn_id,
#                 order_amount=order_amount,
#                 order_id=order_id,
#                 payload=data,
#                 status_time = timestamp,
#                 status_at_receive=status_changed,
#             )
#             return Response({
#                 "message": "Payment Failed",
#                 "order_id": order_id }, status=status.HTTP_200_OK)
#         elif event_type == "PAYMENT_USER_DROPPED_WEBHOOK":
#             WebhookLog.objects.create(
#                 trxn_id=txn_id,
#                 order_amount=order_amount,
#                 order_id=order_id,
#                 payload=data,
#                 status_time = timestamp,
#                 status_at_receive=status_changed,
#             )
#             return Response({
#                 "message": "Payment Dropped",
#                 "order_id": order_id }, status=status.HTTP_200_OK)
#         else :
#             return Response({"message": "Unhandled event"}, status=status.HTTP_400_BAD_REQUEST)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
import json
import hmac
import hashlib
import base64
# SECRET_KEY = "ktvwg6cdy2pd8w8ginsw"


from datetime import datetime
import pytz

def parse_ist_naive(iso_dt_str):
    """Converts ISO 8601 datetime string to naive IST datetime."""
    if not iso_dt_str:
        return None
    india_tz = pytz.timezone("Asia/Kolkata")
    aware_dt = datetime.fromisoformat(iso_dt_str)
    return aware_dt.astimezone(india_tz).replace(tzinfo=None)


class CashfreeWebhook(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # Get webhook data
        received_signature = request.headers.get("x-webhook-signature")
        computed_signature = hmac.new(
            config("WEBHOOK_SECRET_KEY").encode(),
            json.dumps(data, separators=(",", ":")).encode(),
            hashlib.sha256
        ).hexdigest()
        computed_signature_base64 = base64.b64encode(bytes.fromhex(computed_signature)).decode()
        print("computed_signature",computed_signature_base64,"\n received_signature",received_signature)
        if computed_signature_base64 != received_signature:
            print("error : Invalid signature")
        event_type = data.get("type")
        order_id = data.get("data", {}).get("order").get("order_id")
        order_amount = data.get("data", {}).get("order").get("order_amount")
        txn_id = data.get("data", {}).get("payment").get("cf_payment_id")
        timestamp = data.get('event_time')
        status_changed = data.get("data", {}).get("payment").get('payment_status')
        if event_type == "PAYMENT_SUCCESS_WEBHOOK":
            
            
            payment = Payment.objects.get(order_id=order_id)
            payment.status = "SUCCESS"
            payment.transaction_id = txn_id
            payment.save()

            cart_instance = Cart.objects.get(id=payment.cart_id)
            cart_instance.is_active = False
            cart_instance.save()
            address_instance = Address.objects.get(id = payment.address_id)


            WebhookLog.objects.create(
                trxn_id=txn_id,
                order_amount=order_amount,
                order_id=order_id,
                payload=data,
                status_time = timestamp,
                status_at_receive=status_changed,
            )


            Order.objects.create(
                order_id = order_id,
                order_amount = order_amount,
                order_currency = data.get("data", {}).get("order").get("order_currency"),
                customer_id = payment.customer_id,
                customer_phone = payment.customer_phone,
                cart_id = cart_instance , #     int(payment.cart_id),
                address_id =  address_instance , #  int(payment.address_id),
                status = status_changed,
                payment_mode = data.get("data", {}).get("payment").get("payment_method") ,
                payment_time = parse_ist_naive(data.get("data", {}).get("payment").get("payment_time")),
                transaction_id = txn_id,
                return_url = 'https://ahufcafe.com/',
                notify_url = 'https://ahufcafe.com/'
            )
            
            
            
            return Response({
                "message": "Payment received",
                "order_id": order_id }, status=status.HTTP_200_OK)
        elif event_type == "PAYMENT_FAILED_WEBHOOK":
            WebhookLog.objects.create(
                trxn_id=txn_id,
                order_amount=order_amount,
                order_id=order_id,
                payload=data,
                status_time = timestamp,
                status_at_receive=status_changed,
            )
            return Response({
                "message": "Payment Failed",
                "order_id": order_id }, status=status.HTTP_200_OK)
        elif event_type == "PAYMENT_USER_DROPPED_WEBHOOK":
            WebhookLog.objects.create(
                trxn_id=txn_id,
                order_amount=order_amount,
                order_id=order_id,
                payload=data,
                status_time = timestamp,
                status_at_receive=status_changed,
            )
            return Response({
                "message": "Payment Dropped",
                "order_id": order_id }, status=status.HTTP_200_OK)
        else :
            return Response({"message": "Unhandled event"}, status=status.HTTP_400_BAD_REQUEST)
            
class ProfilePage(APIView):


    def get(self,request):
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        if user.is_authenticated :
            userDetails = UserDetails.objects.get(currentUser = user)

            return render(request , 'mainProfile.html' , context={"user":user , "userDetails":userDetails } )
        else :
            return redirect('login-page')
        

class ProfileOredersPage(APIView):
    def get(self,request):    
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        if user.is_authenticated :
            
            Current_orders = Order.objects.filter(customer_id = "cust_0"+str(user.id), order_active = False)
            serializer =  OrderSerializer(Current_orders, many=True, context={"request": request , "include_cart":True , "include_address" : True })


            return render(request , 'orders.html' , context={"orders_hist":serializer.data})
        else :
            return redirect('login-page')





class ProfileAddressPage(APIView):
    def get(self,request):    
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        if user.is_authenticated :

            addresses = Address.objects.filter(user=user)
            serializer = AddressSerializer(addresses, many=True)
            context = {
                "user": user ,
                "address_data": serializer.data
            }  

            return render(request , 'address.html' , context )
        else :
            return redirect('login-page')


class ProfileSupportPage(APIView):
    def get(self,request):    
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        if user.is_authenticated :

            return render(request , 'support.html')
        else :
            return redirect('login-page')


import logging

logger = logging.getLogger('Ahuf_app')


class LogView(APIView):
    def get(self, request, *args, **kwargs):
        logger.debug("This is a debug log test.")
        logger.error("This is an error log test.")
        return Response({"message": "Logs have been written."})
        
        
class ProfileTrackOrders(APIView):
    def get(self,request):
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        if user.is_authenticated :

            Current_orders = Order.objects.filter(customer_id = "cust_0"+str(user.id), order_active = True).order_by('-created_at')
            serializer =  OrderSerializer(Current_orders, many=True, context={"request": request , "include_cart":True , "include_address" : True })

            
            return render(request , 'track-order.html' ,  context={"orders":serializer.data})
        else :
            return redirect('login-page')
            
            
class GetOrdersHistory(APIView):
    def get(self,request):
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        if user.is_authenticated :
            Current_orders = Order.objects.all()
            serializer =  OrderSerializer(Current_orders , many=True, context={"request": request})
            # print(serializer.data)

            return Response({"success": True,
                              "message": "Orders Fetched SuccessFully.",
                              "data":serializer.data
                              }, status=200)
        else:
            return Response({"success": False,
                              "message": "Some Issue."}, status=400)


class ChangeOrderStatus(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        flow = ["In Progress" ,'IN_PROGRESS' , 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED']


        order_id = request.data.get('order_id')
        status = request.data.get('status')
        order = Order.objects.get(order_id=order_id)
        current = order.order_status

        if status not in ['PREPARING','OUT_FOR_DELIVERY','DELIVERED','CANCELED']:
            return Response({"success": False,
                            "message": "Invalid Status."}, status=400)
        elif order_id is None:
            return Response({"success": False,
                            "message": "Order ID is required."}, status=400)
        
        elif Order.objects.filter(order_id=order_id).exists() is False:
            return Response({"success": False,
                            "message": "Order ID does not exist."}, status=400)
        
        elif Order.objects.filter(order_id=order_id).first().order_status == 'DELIVERED':
            return Response({"success": False,
                            "message": "Order is already delivered."}, status=400)
        elif Order.objects.filter(order_id=order_id).first().order_status == 'CANCELED':
            return Response({"success": False,
                            "message": "Order is already canceled."}, status=400)
        elif status == 'CANCELED':
            order = Order.objects.get(order_id=order_id)
            order.order_status = status
            order.order_active = False
            order.save()
            return Response({"success": True,
                            "message": "Order Status Changed SuccessFully.",
                            }, status=200)
        elif flow.index(status) >= flow.index(current):
            
            order = Order.objects.get(order_id=order_id)
            if status == 'DELIVERED':
                order.order_active = False
            order.order_status = status
            order.save()
            return Response({"success": True,
                            "message": "Order Status Changed SuccessFully.",
                            }, status=200)
        else:
            return Response({"success": False,
                              "message": "Some Issue."}, status=400)


class OrderDetailsPage(APIView):
    def get(self, request):
        # access_token = request.COOKIES.get('access_token')
        # user = AnonymousUser()
        # if access_token:
        #     try:
        #         auth = JWTAuthentication()
        #         validated_token = auth.get_validated_token(access_token)
        #         user = auth.get_user(validated_token)
        #     except (InvalidToken, TokenError) as e:
        #         print("Invalid Token:", str(e))

        # if user.is_authenticated :
        order = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(order , many=True, context={"request": request, "include_cart":True, "include_address" : True })
        print(serializer.data)

        return render(request, 'order-details.html', context={"order":serializer.data})
        # else :
        #     return redirect('login-page')
        
class GetDetailsByOrderId(APIView):
    def post(self,request):

        ahuf_order_id = request.data.get('ahuf_order_id')
        if ahuf_order_id is None:
            return Response({"success": False,
                            "message": "Order ID is required."}, status=400)

        elif Order.objects.filter(ahuf_order_id=ahuf_order_id).exists() is False:
            return Response({"success": False,
                            "message": "Order ID does not exist."}, status=400)

        else:
            order = Order.objects.get(ahuf_order_id=ahuf_order_id)
            serializer = OrderSerializer(order, context={"request": request, "include_cart":True, "include_address" : True })
            return Response({"success": True,
                            "message": "Order Fetched SuccessFully.",
                            "data":serializer.data
                            }, status=200)
                            
                            
class ChangeOrderStatus(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        
        flow = ["In Progress" ,'IN_PROGRESS' , 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED']


        ahuf_order_id = request.data.get('ahuf_order_id')
        status = request.data.get('status')
        order = Order.objects.get(ahuf_order_id=ahuf_order_id)
        current = order.order_status

        if status not in ['PREPARING','OUT_FOR_DELIVERY','DELIVERED','CANCELED']:
            return Response({"success": False,
                            "message": "Invalid Status."}, status=400)
        elif ahuf_order_id is None:
            return Response({"success": False,
                            "message": "Order ID is required."}, status=400)
        
        elif Order.objects.filter(ahuf_order_id=ahuf_order_id).exists() is False:
            return Response({"success": False,
                            "message": "Order ID does not exist."}, status=400)
        
        elif Order.objects.filter(ahuf_order_id=ahuf_order_id).first().order_status == 'DELIVERED':
            return Response({"success": False,
                            "message": "Order is already delivered."}, status=400)
        elif Order.objects.filter(ahuf_order_id=ahuf_order_id).first().order_status == 'CANCELED':
            return Response({"success": False,
                            "message": "Order is already canceled."}, status=400)
        elif status == 'CANCELED':
            order = Order.objects.get(ahuf_order_id=ahuf_order_id)
            order.order_status = status
            order.order_active = False
            order.save()
            return Response({"success": True,
                            "message": "Order Status Changed SuccessFully.",
                            }, status=200)
        elif flow.index(status) >= flow.index(current):
            
            order = Order.objects.get(ahuf_order_id=ahuf_order_id)
            if status == 'DELIVERED':
                order.order_active = False
            order.order_status = status
            order.save()
            return Response({"success": True,
                            "message": "Order Status Changed SuccessFully.",
                            }, status=200)
        else:
            return Response({"success": False,
                              "message": "Some Issue."}, status=400)
                              
                              
# ================================== Combo API ========================================

class ComboPageView(APIView):
    def get(self, request ):
        
        access_token = request.COOKIES.get('access_token')
        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))
        
        Category_data = Category.objects.all()
        Combo_Category_data = ComboCategory.objects.filter(for_catering = True)
        serializers_caty_data = ComboCategorySerializer(Combo_Category_data, many=True)
        serializers_data = CategoryWithSubSerializer(Category_data, many=True)
        context = {
            'combo_categories' : serializers_caty_data.data,
            'categories': serializers_data.data,
            "user": user
        }
        return render(request , 'combo-page.html' , context)
    

class ComboCategoriesData(APIView):
    def get(self, request):
        Category_data = ComboCategory.objects.all()
        serializers_data = ComboCategorySerializer(Category_data, many=True)
        return Response({"success": True,
                         "message": "Categories Fetched SuccessFully.",
                         "data": serializers_data.data
                         }, status=200)


class ComboCategoriesParty(APIView):
    def get(self, request):
        Category_data = ComboCategory.objects.filter(for_catering = True)
        serializers_data = ComboCategorySerializer(Category_data, many=True)
        return Response({"success": True,
                         "message": "Categories Fetched SuccessFully.",
                         "data": serializers_data.data
                         }, status=200)

class ComboMenuData(APIView):
    def get(self,request):

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            access_token = auth_header.split('Bearer ')[1]
        else:
            access_token = None

        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        
            
        print(access_token, user)
        Combo_category_id = request.query_params.get('category_id')
        item_id = request.query_params.get('item_id')
        is_party_catering = request.query_params.get('is_party_catering','false')
        is_party_catering = True if is_party_catering == 'true' else False
        
        if Combo_category_id:
            combo_menu = ComboMenu.objects.filter(is_active = True , category = Combo_category_id , for_catering = is_party_catering)
        elif item_id:
            combo_menu = ComboMenu.objects.filter(is_active = True , id = item_id , for_catering = is_party_catering)
        else:
            combo_menu = ComboMenu.objects.filter(is_active = True)
        if user.is_authenticated :
            print("i am from auth")
            serializer = ComboMenuSerializer(combo_menu, many=True , context={'user': user , "is_party_catering":is_party_catering })
        else:
            serializer = ComboMenuSerializer(combo_menu, many=True , context={"is_party_catering":is_party_catering} )

        return Response({"success": True,
                         "message": "Combo Menu Fetched SuccessFully.",
                         "data": serializer.data
                         }, status=200)

        
        
class ComboPageMainView(APIView):
    def get(self, request):

        access_token = request.COOKIES.get('access_token')

        user = AnonymousUser()
        if access_token:
            try:
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                print("Invalid Token:", str(e))

        Combo_Category_data = ComboCategory.objects.filter(for_catering = False)
        serializers_caty_data = ComboCategorySerializer(Combo_Category_data, many=True)
        Category_data = Category.objects.all()
        serializers_data = CategoryWithSubSerializer(Category_data, many=True)
        
            
        context = {
            'combo_categories' : serializers_caty_data.data,
            'categories': serializers_data.data,
            "user" : user
        }
        return render(request, 'combo-main-page.html' ,context )

# ==================================== Shedule ===============

class UpdateCartScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user, is_active=True, is_party_catering=True)
        except Cart.DoesNotExist:
            return Response({"error": "Active party catering cart not found."}, status=404)

        serializer = OrderScheduleSerializer(data=request.data)
        if serializer.is_valid():
            # Update existing schedule or create new
            schedule, _ = OrderSchedule.objects.update_or_create(
                cart=cart,
                defaults=serializer.validated_data
            )
            return Response({
                "success": True,
                "message": "Schedule saved successfully.",
                "data": serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)
        

class OtpCheckAPi(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        myotp = '172914'
        if otp is None:
            return Response({"success": False,
                            "message": "OTP is required."}, status=400)
        elif otp != myotp:
            return Response({"success": False,
                            "message": "OTP is not valid."}, status=400)
        else:
            return Response({"success": True,
                            "message": "OTP is valid.",
                            }, status=200)

        
        