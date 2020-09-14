from rest_framework import routers
from .views import HomeView


router = routers.DefaultRouter()
router.register('', HomeView)

urlpatterns = router.urls