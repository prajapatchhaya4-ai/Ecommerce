from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view,register_view,add_to_cart,indexpage,cart_details,remove_from_cart,increase_quantity,decrease_quantity,search,category_products, subcategory_products,product_detail,master,logout_view

urlpatterns = [
    path('',indexpage,name="index" ),
    path('master/',master,name="master"),
    # path('home/',homepage,name="home"),
    path('cartdetails/',cart_details,name="cartdetails"),
    path('delete/<int:id>/',remove_from_cart,name="delete"),
    path('cart_add/<int:id>/',add_to_cart,name="cart_add"),
    path('decrease/<int:id>/',decrease_quantity, name='decrease_quantity'),
    path("search/", search, name="search"),
    path("category/<int:id>/",category_products, name="category_products"),
    path("subcategory/<int:id>/", subcategory_products, name="subcategory_products"),
    path(" productdetail/<int:id>/",  product_detail, name="product_detail"),
    path('increase/<int:id>/',increase_quantity, name='increase_quantity'),
    
    path('login/',login_view,name="signin"),
    path('register/',register_view,name="signup"),
    path('logout/',logout_view,name="logout")

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)