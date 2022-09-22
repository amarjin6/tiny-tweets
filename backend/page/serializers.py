from rest_framework import serializers

from page.models import Tag, Page, Post
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class FullPageSerializer(serializers.ModelSerializer):
    tags = TagSerializer()
    owner = UserSerializer()
    followers = UserSerializer()

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'is_private', 'is_blocked', 'unblock_date')


class PageSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    owner = UserSerializer()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'is_private', 'is_blocked', 'unblock_date')
        read_only_fields = ('followers', 'is_blocked', 'unblock_date')

    def get_followers(self, obj):
        response = []
        for _user in obj.all():
            follower_profile = UserSerializer(
                _user.userprofile,
                context={'request': self.context['request']})
            response.append(follower_profile.data)
        return response


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'created_at', 'updated_at')
