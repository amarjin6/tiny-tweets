from rest_framework import routers

from page.views import TagViewSet, PageViewSet, PostViewSet
from user.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'pages', PageViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
