from django.contrib import admin
from django.urls import path, include

from schoolmock_app.urls import router
from schoolmock_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schoolmock_app.urls')),
    path('api/', include(router.urls)),
]