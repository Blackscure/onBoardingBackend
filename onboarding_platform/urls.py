from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apps/monday-donations/api/v1/authentication/', include('authentication.api.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
