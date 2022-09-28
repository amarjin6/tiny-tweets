from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from page.models import Tag, Page, Post
from page.permissions import PageAccessPermission
from page.serializers import TagSerializer, PageSerializer, PostSerializer, FullPageSerializer, CreatePageSerializer
from page.filters import PageFilter


class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, PageAccessPermission)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PageFilter

    serializer_action_classes = {
        'create': CreatePageSerializer,
    }

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullPageSerializer
        return self.serializer_action_classes.get(self.action, self.serializer_class)

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'owner': User.objects.get(id=self.request.user.id)}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
