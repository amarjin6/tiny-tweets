from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from core.mixins.serializers import DynamicRoleSerializerMixin
from core.enums import Role
from page.models import Tag, Page, Post
from page.permissions import PageAccessPermission
from page.serializers import TagSerializer, PageSerializer, PostSerializer, FullPageSerializer
from page.filters import PageFilter


class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


class PageViewSet(DynamicRoleSerializerMixin, viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, PageAccessPermission)

    serializer_role_classes = {
        Role.ADMIN.value: FullPageSerializer,
        Role.MODERATOR.value: FullPageSerializer,
    }

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PageFilter


class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
