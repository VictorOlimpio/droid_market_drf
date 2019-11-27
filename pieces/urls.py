from django.conf.urls import url, include
from rest_framework import routers
from pieces.views import PieceVewSet

router = routers.DefaultRouter()
router.register(r'pieces', PieceVewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]