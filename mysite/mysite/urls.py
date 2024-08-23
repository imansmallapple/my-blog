from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from utils.upload import upload_file
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('blog.urls')),
    path('uploads/', upload_file, name='uploads')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
