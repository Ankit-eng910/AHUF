
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * # CategoryViewSet, SubCategoryViewSet, MenuItemViewSet





urlpatterns = [
    # path('', include(router.urls)),
    path('categories/', CategoryViewSet.as_view(), name='category-list'),
    path('get-filter-categories/', GetFilterCategories.as_view(), name='get-filter-categories'),
    path('menu-items/', MenuItemAdd.as_view(), name='menu-item-add'),
    path('add-subcategory/', SubCategoryViewSet.as_view(), name='add-subcategory'),
    path('get-menu-items/', GetMenuItems.as_view(), name='get-menu-items'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategories'),
    path('update-category/<int:pk>/', CategoryUpdate.as_view(), name='update-category'),
    path('recomdated-menu/', RecomdatedMenu.as_view(), name='recomdated-menu'),
    path("searchmenu/", SearchMenu.as_view(), name="menuSearch"),

    path('add-cart/',AddOrUpdateCartItemView.as_view(), name='addcart'),
    path('get-cart/', GetCartView.as_view(),name='getCart'),
    path('remove-item/' , RemoveCartItem.as_view() , name='removeitem'),

    path('otpless-login/', UserLoginView.as_view() , name = "userLogin"),

    # path('home-page/', HomePageView.as_view(), name='home-page'),
    # path('blog-page/<int:MenuId>/', BlogPageView.as_view(), name='blog-page'),
    path('blog-page/', BlogPageView.as_view(), name='blog-page'),
    path('about-page/', AboutPageView.as_view(), name='about-page'),
    path('login-page/' , LoginPageView.as_view() , name = 'login-page'  ),
    path('view-cartPage/', ViewCartPageView.as_view(), name = 'viewCart-page'),
    path('menu-detils/<str:category>/<str:subcategory>/<str:item_name>/', MenuDetailsPage.as_view() , name='menu-page'),
    # path("error/",Html404Page,name='Error-page'),
    # path('test-log/', TestLogView.as_view(), name='test-log'),

    # path("menubarBase/", menubarBase.as_view(), name="menubarBase"),
    path("Cancellation-&-Refund-Policy/" , RefundPolicy.as_view() ,name='refundPolicy' ),
    path("Terms-&-Conditions/" , TermAndConditions.as_view() , name="terms&Conditions"),
    path('offers/', OfferAPIView.as_view(),name='offer'),
    path('code/', CodeAPIView.as_view(),name='code'),
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/update/', AddressUpdateAPIView.as_view(), name='address-update'),
   
    path('addresses/<int:pk>/delete/', AddressDeleteAPIView.as_view(), name='address-delete'),
    
    
    path('pay/', paymentpage.as_view(), name='initiate_payment'),
    path("cashfree/webhook/", CashfreeWebhook.as_view(), name="cashfree-webhook"),
    
    path('Get-orders/',GetOrdersHistory.as_view() ,name='Orders-fetch' ),
    # path('Current-orders/', CurrentOrder.as_view() , name='currentOreder'),


    path('getOrders-by-id/' ,GetDetailsByOrderId.as_view() , name='ordersbyid'),

    path('change-order-status/' , ChangeOrderStatus.as_view(), name='changeOrderStatus'),


    # path('test-onboard/' , GetMunuData.as_view() , name='test-bro'),


    # ==========================================================================

    path('schedule-orders/', UpdateCartScheduleView.as_view(), name='scheduleOrders'),

]
