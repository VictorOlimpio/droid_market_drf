from django.conf.urls import url, include
from rest_framework import routers
from pieces.views import PieceViewSet

router = routers.DefaultRouter()
router.register(r'pieces', PieceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]