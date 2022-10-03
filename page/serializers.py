from rest_framework import serializers

from page.models import Tag, Page, Post
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class BlockPageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret['is_blocked']:
            return ret


class FullPageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(many=True)
    follow_requests = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'title', 'tags', 'owner', 'followers', 'follow_requests', 'is_private', 'is_blocked',
                  'unblock_date')


class PageSerializer(BlockPageSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = (
            'id', 'uuid', 'title', 'tags', 'image', 'description', 'owner', 'followers', 'is_private', 'is_blocked',
            'unblock_date')
        read_only_fields = ('followers', 'is_blocked', 'unblock_date')


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


class PageOwnerSerializer(BlockPageSerializer, serializers.ModelSerializer):
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


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'created_at', 'updated_at', 'reply_to', 'liked_by')


class CreatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'owner', 'reply_to')

        def create(self, validated_data):
            return Post.objects.create(**validated_data)


class UpdatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'owner', 'reply_to')


class LikedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'page_post')
        depth = 1

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        posts = ret.pop('page_post')
        i = 0
        for post in posts:
            if not post['liked_by']:
                posts.pop(i)

            i += 1

        ret['page_post'] = posts
        return ret
