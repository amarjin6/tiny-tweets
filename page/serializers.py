from rest_framework import serializers

from page.models import Tag, Page, Post
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class FullPageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(many=True)
    follow_requests = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'follow_requests', 'is_private', 'is_blocked',
                  'unblock_date')


class PageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = (
            'id', 'uuid', 'title', 'tags', 'image', 'description', 'owner', 'followers', 'is_private', 'is_blocked',
            'unblock_date')
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


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'image', 'owner', 'description', 'is_private')


class PageOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'description', 'followers', 'follow_requests', 'is_private',
                  'is_blocked', 'unblock_date')
        read_only_fields = ('is_blocked', 'unblock_date')


class ApproveRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests', 'followers')

    def update(self, page, validated_data):
        users = validated_data.pop('follow_requests')
        for user in users:
            page.follow_requests.remove(user)
            page.followers.add(user)

        page.save()
        return page


class DeclineRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests',)

    def update(self, page, validated_data):
        users = validated_data.pop('follow_requests')
        for user in users:
            page.follow_requests.remove(user)

        page.save()
        return page
