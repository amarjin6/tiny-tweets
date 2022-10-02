import os
from django.core.mail import send_mail


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
    def block_pages(request):
        ...


class PostService:
    @staticmethod
    def like_unlike_switch(post, request):
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            msg = {'status': 'You like this post'}

        else:
            post.liked_by.remove(request.user)
            msg = {'status': 'You don\'t like this post anymore'}

        return msg


class UploadService:
    @staticmethod
    def check_file_extension(request):
        ...

    @staticmethod
    def send_email(emails_list: list, msg: str):
        send_mail(
            os.getenv('SUBJECT', 'Innotter notification'),
            msg,
            os.getenv('EMAIL_HOST_USER'),
            emails_list,
            fail_silently=False
        )
