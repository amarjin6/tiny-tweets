from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.hashers import make_password

from user.models import User
from user.serializers import UserSerializer, CreateUserSerializer
from core.mixins.serializers import DynamicActionSerializerMixin
from core.permissions import IsAdminOrModerator
from user.filters import UserFilter


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
