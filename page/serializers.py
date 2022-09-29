from rest_framework import serializers

from page.models import Tag, Page, Post
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class FullPageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    owner = UserSerializer()
    followers = UserSerializer(many=True)

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'is_private', 'is_blocked', 'unblock_date')


class PageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    owner = UserSerializer()
    followers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'is_private', 'is_blocked', 'unblock_date')
        read_only_fields = ('followers', 'is_blocked', 'unblock_date')


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'created_at', 'updated_at')


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'image', 'owner', 'description', 'is_private')

        def create(self, validated_data):
            return Page.objects.create(**validated_data)
