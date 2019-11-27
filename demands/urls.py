from django.conf.urls import url, include
from rest_framework import routers
from demands.views import DemandViewSet

router = routers.DefaultRouter()
router.register(r'demands', DemandViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]