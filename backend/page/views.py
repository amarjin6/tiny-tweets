from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from page.models import Tag, Page, Post
from page.serializers import TagSerializer, PageSerializer, PostSerializer


class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


class PageViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated,)


class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
