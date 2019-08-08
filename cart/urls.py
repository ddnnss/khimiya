
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_from_main_cart/', views.delete_from_main_cart, name='delete_from_main_cart'),
    path('use_promo/', views.use_promo, name='use_promo'),
    path('sort_filter/', views.sort_filter, name='sort_filter'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('wishlist_add/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete/', views.wishlist_delete, name='wishlist_delete'),


]
