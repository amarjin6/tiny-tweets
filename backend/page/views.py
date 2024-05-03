from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from core.mixins.serializers import DynamicActionSerializerMixin
from page.models import Tag, Page, Post
from page.permissions import PageAccessPermission, IsPageOwner
from page.serializers import TagSerializer, PageSerializer, PostSerializer, FullPageSerializer, CreatePageSerializer, \
    UpdatePageSerializer, PageOwnerSerializer, ApproveRequestsSerializer, DeclineRequestsSerializer, \
    CreatePostSerializer, UpdatePostSerializer, LikedPostsSerializer
from page.filters import PageFilter
from page.services import PageService, PostService, TagService
from page.tasks import send_mail
from core.serializers import ImageSerializer
from core.services import AWSManager
from page.producer import publish
from microservice.enums import MessageType


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
        tags_id = TagService.process_tags(request)
        image = None
        if 'image' in request.data:
            ImageSerializer.validate_extension(request.data['image'])
            image = AWSManager.upload_file(self.request.data['image'], 'page' + str(Page.objects.latest('id').id + 1))

        data = {**request.data, 'tags': tags_id, 'image': image, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        publish({**serializer.data, 'type': MessageType.CREATE.value})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        tags_id = TagService.process_tags(request)
        data = {**request.data, 'tags': tags_id, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        publish({**serializer.data, 'type': MessageType.UPDATE.value})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        serializer = PageSerializer(self.queryset, many=True)
        for page in serializer.data:
            page['image'] = AWSManager.create_presigned_url(key=page['image'])
        return Response(serializer.data)

    def retrieve(self, request, pk):
        page = get_object_or_404(self.queryset, pk=pk)
        serializer = PageSerializer(page)
        data = serializer.data
        image = AWSManager.create_presigned_url(key=data['image'])
        data['image'] = image
        return Response(data)

    def perform_destroy(self, instance):
        publish({'id': instance.id, 'type': MessageType.DELETE.value})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    @action(methods=['PATCH'], url_path='decline-requests', permission_classes=[IsPageOwner],
            detail=True)
    def decline_requests(self, request, *args, **kwargs):
        serializer = DeclineRequestsSerializer(self.get_object(), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path='liked-posts', permission_classes=[PageAccessPermission],
            detail=True)
    def show_liked_posts(self, request, *args, **kwargs):
        serializer = LikedPostsSerializer(self.get_object(), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(DynamicActionSerializerMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    serializer_action_classes = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer,
    }

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_mail.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path=r'\w*like', permission_classes=[IsAuthenticated], detail=True)
    def like(self, request, *args, **kwargs):
        msg = PostService.like_unlike_switch(self.get_object(), request)
        return Response(data=msg, status=status.HTTP_201_CREATED)


class FeedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(page__owner=self.request.user.id or Post(page__followers=self.request.user.id),
                                   page__owner__is_blocked=False,
                                   page__is_blocked=False).order_by('-created_at')
