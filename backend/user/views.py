from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
