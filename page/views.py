from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from user.models import User
from page.models import Tag, Page, Post
from page.permissions import PageAccessPermission, IsPageOwner
from page.serializers import TagSerializer, PageSerializer, PostSerializer, FullPageSerializer, CreatePageSerializer, \
    UpdatePageSerializer, PageOwnerSerializer, ApproveRequestsSerializer
from page.filters import PageFilter
from page.services import PageService


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
        'update': UpdatePageSerializer,
    }

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullPageSerializer
        try:
            if self.request.user == self.get_object().owner:
                return PageOwnerSerializer
        except AssertionError:
            return self.serializer_action_classes.get(self.action, self.serializer_class)

    def create(self, request, *args, **kwargs):
        tags = request.data.pop('tags')
        tags_id = []
        for tag in tags:
            try:
                obj = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                obj = Tag.objects.create(name=tag)
                obj.save()
            tags_id.append(obj.id)

        data = {**request.data, 'tags': tags_id, 'owner': User.objects.get(id=self.request.user.id).id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        tags = request.data.pop('tags')
        tags_id = []
        for tag in tags:
            try:
                obj = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                obj = Tag.objects.create(name=tag)
                obj.save()
            tags_id.append(obj.id)

        data = {**request.data, 'tags': tags_id, 'owner': User.objects.get(id=self.request.user.id).id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @action(methods=['GET'], url_path=r'\w*follow', permission_classes=[IsAuthenticated], detail=True)
    def follow(self, request, *args, **kwargs):
        msg = PageService.follow_unfollow_switch(self.get_object(), request)
        return Response(data=msg, status=status.HTTP_201_CREATED)

    @action(methods=['PATCH'], url_path='approve-requests', permission_classes=[IsPageOwner],
            detail=True)
    def approve_requests(self, request, *args, **kwargs):
        serializer = ApproveRequestsSerializer(self.get_object(), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
