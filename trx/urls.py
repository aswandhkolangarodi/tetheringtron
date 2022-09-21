

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from member import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('trxadmin/',include('trxadmin.urls')),
    path('member/', include('member.urls')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.handler404