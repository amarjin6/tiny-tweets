from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from user.models import User
from user.serializers import UserSerializer, CreateUserSerializer
from core.mixins.serializers import DynamicActionSerializerMixin
from core.permissions import IsAdminOrModerator


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

    def get_permissions(self):
        for actions, permission in self.permissions_mapping.items():
            if self.action in actions:
                self.permission_classes = (permission,)
        return super(self.__class__, self).get_permissions()
