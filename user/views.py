from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from user.serializers import UserSerializer, CreateUserSerializer
from core.mixins.serializers import DynamicActionSerializerMixin
from core.permissions import IsAdminOrModerator
from user.filters import UserFilter
from page.services import PageService


class UserViewSet(DynamicActionSerializerMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    permissions_mapping = {
        'create': AllowAny,
        'retrieve': IsAdminOrModerator,
        'update': IsAdminOrModerator,
        'destroy': IsAdminUser,
        'list': IsAdminOrModerator,
    }
    serializer_action_classes = {
        'create': CreateUserSerializer,
    }

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def get_permissions(self):
        for actions, permission in self.permissions_mapping.items():
            if self.action in actions:
                self.permission_classes = (permission,)
        return super(self.__class__, self).get_permissions()

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.data['is_blocked']:
            PageService.block_pages(user_id=kwargs['pk'])
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)
