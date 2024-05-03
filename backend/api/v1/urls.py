from rest_framework import routers

from page.views import TagViewSet, PageViewSet, PostViewSet, FeedViewSet
from user.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'tags', TagViewSet)
router.register(r'pages', PageViewSet, basename='Page')
router.register(r'posts', PostViewSet)
router.register(r'register', UserViewSet)
router.register(r'feed', FeedViewSet, basename='Feed')

urlpatterns = router.urls
