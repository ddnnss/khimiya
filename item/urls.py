
from django.urls import path
from . import views

urlpatterns = [
    path('quick_view/', views.quick_view, name='quick_view'),
    path('<item_slug>/', views.item_page, name='item_page'),

]
