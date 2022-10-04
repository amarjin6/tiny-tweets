import os
from django.core.mail import send_mail

from page.models import Page


class PageService:
    @staticmethod
    def follow_unfollow_switch(page, request) -> dict:
        if request.user not in page.followers.all():
            if page.is_private:
                page.follow_requests.add(request.user)
                msg = {'status': 'Follow request created'}

            else:
                page.followers.add(request.user)
                msg = {'status': 'Now you follow this page'}

        else:
            page.followers.remove(request.user)
            msg = {'status': 'You are no longer follow this page'}

        return msg

    @staticmethod
    def block_unblock_switch(user_id: int, is_blocked: bool):
        pages = Page.objects.select_related('owner').filter(owner_id=user_id)
        for page in pages:
            if is_blocked and not page.is_blocked:
                page.is_blocked = True
            elif not is_blocked and page.is_blocked:
                page.is_blocked = False
            page.save()


class PostService:
    @staticmethod
    def like_unlike_switch(post, request) -> dict:
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            msg = {'status': 'You like this post'}

        else:
            post.liked_by.remove(request.user)
            msg = {'status': 'You don\'t like this post anymore'}

        return msg


class NotificationService:
    @staticmethod
    def send_email(emails_list: list, msg: str):
        send_mail(
            os.getenv('SUBJECT', 'Innotter notification'),
            msg,
            os.getenv('EMAIL_HOST_USER'),
            emails_list,
            fail_silently=False
        )
