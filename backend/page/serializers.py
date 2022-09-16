from rest_framework import serializers

from page.models import Tag, Page, Post
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PageSerializer(serializers.ModelSerializer):
    tags = TagSerializer()
    owner = UserSerializer()
    followers = UserSerializer()

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'is_private', 'unblock_date')


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'created_at', 'updated_at')
