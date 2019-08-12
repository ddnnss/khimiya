from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


from page.views import customhandler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page.urls')),
    path('item/', include('item.urls')),
    path('cart/', include('cart.urls')),
    path('user/', include('customuser.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = customhandler404