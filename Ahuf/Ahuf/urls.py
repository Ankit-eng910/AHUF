"""
URL configuration for Ahuf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from Ahuf_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Ahuf_app.urls')),
     path('OAHUF/', include('OAhuf_app.urls')),
    path('', MainHomePageView.as_view(), name='home'),
    path('response/', payment_response_view, name='payment-response'),
    path('Profile/', ProfilePage.as_view() , name='pro'),
    path('orders/', ProfileOredersPage.as_view() , name='orders'),
    path('address/', ProfileAddressPage.as_view() , name='add'),
    path('support/', ProfileSupportPage.as_view() , name='support'),
    path('trackorders/',ProfileTrackOrders.as_view() , name='trackOrder'),
    path('order-detail/',OrderDetailsPage.as_view() , name="orderDetail"),


    path('party-catering/', ComboPageView.as_view() , name='combo'),


    path('error/' ,Html404Page , name='error' ),


#============================ Important ===========================================#
    # path('Important/',AssignCustomerIDView.as_view() , name='assignCustomerID'),
    # path('Important2/', AllocateAhufOrderID.as_view(), name='assignCustomerID2'),

    path('combo-categories/' , ComboCategoriesData.as_view() , name='ComboCategory') ,
    path('combo-categories-party/' , ComboCategoriesParty.as_view() , name='Party-Combo-categories'),
    path('combo-data/' , ComboMenuData.as_view() , name='combo_data'),

    path('combo-main-page/' , ComboPageMainView.as_view() , name='combo-main-page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Ahuf_app.views.Html404Page'
