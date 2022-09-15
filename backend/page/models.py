from django.db import models

from user.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='tags_page')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_page')
    followers = models.ManyToManyField(User, related_name='followers_page')
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(User, related_name='follow_requests_page')
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.uuid} {self.title}'


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_post')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='reply_to_post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page.title
