from django.conf.urls import url, include
from rest_framework import routers
from pieces.views import PiecesVewSet

router = routers.DefaultRouter()
router.register(r'pieces', PiecesVewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]