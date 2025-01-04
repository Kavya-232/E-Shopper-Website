
from django.contrib import admin
from django.urls import include, path
from .import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', views.Master, name = 'master'),
    path('',views.Index, name = "index"),
    path('signup',views.signup, name='signup'),
    path('accounts/login/', LoginView.as_view(template_name='register/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

     
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart_detail/',views.cart_detail,name='cart_detail'),


     path('checkout/', views.Checkout, name = "checkout"),
    path('contact_us',views.Contact_page,name='contact_page'),
     path('order/',views.Your_order,name = 'order'),
     path('product/',views.Product_page,name='product'),
    path('product/<str:id>/', views.product_detail, name='product_detail'),

    path('search/', views.Search, name = 'search'),
] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

