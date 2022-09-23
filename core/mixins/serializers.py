class DynamicActionSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, self.serializer_class)


class DynamicRoleSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_role_classes.get(self.request.user.role, self.serializer_class)
