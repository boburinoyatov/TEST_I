from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'tests', TestViewSet)

urlpatterns = [
    path('', home, name="home"),
    path('accounts/', include('accounts.urls')),
]
