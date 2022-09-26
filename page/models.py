import uuid
from django.db import models

from user.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    uuid = models.CharField(unique=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=80)
    tags = models.ManyToManyField(Tag, related_name='tags_page')
    image = models.URLField(null=True, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_page')
    followers = models.ManyToManyField(User, related_name='followers_page', blank=True)
    follow_requests = models.ManyToManyField(User, related_name='follow_requests_page', blank=True)
    is_private = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.uuid} {self.title}'


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_post')
    content = models.CharField(max_length=180)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_post')
    liked_by = models.ManyToManyField(User, related_name='liked_by_post', blank=True)
    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='reply_to_post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page.title
