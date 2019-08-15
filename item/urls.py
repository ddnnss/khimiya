
from django.urls import path
from . import views

urlpatterns = [
    path('quick_add_to_cart/', views.quick_add_to_cart, name='quick_add_to_cart'),
#    path('<item_slug>/', views.item_page, name='item_page'),


]
