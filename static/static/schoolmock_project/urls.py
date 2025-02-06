from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from schoolmock_app.urls import router
from schoolmock_app.views import *
from schoolmock_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schoolmock_app.urls')),
    path('api/', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # new
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # new