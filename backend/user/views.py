from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.models import User
from user.serializers import UserSerializer, CreateUserSerializer
from core.mixins.permissions import PermissionMixin
from core.mixins.serializers import DynamicSerializerMixin


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
                  PermissionMixin, DynamicSerializerMixin):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    permissions_mapping = {
        'create': AllowAny,
    }
    serializer_action_classes = {
        'create': CreateUserSerializer,
    }
