
from django.urls import path
from . import views

urlpatterns = [
   path('log_in/', views.log_in, name='log_in'),
   path('logout/', views.log_out, name='logout'),
   path('signup/', views.signup, name='signup'),
   path('restore/', views.restore, name='restore'),
   path('account/', views.account, name='account'),
   path('account/edit', views.account_edit, name='account_edit'),
   path('account/wishlist', views.wishlist, name='wishlist'),
   path('account/orders', views.orders, name='orders'),
   path('account/order/<order_code>', views.order, name='order'),

]
