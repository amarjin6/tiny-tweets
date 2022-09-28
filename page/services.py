import os

from django.core.mail import send_mail


class PageService:
    @staticmethod
    def follow_unfollow_switch(page, request) -> str:
        if request.user not in page.followers.all():
            if page.is_private:
                page.follow_requests.add(request.user)
                msg = 'Waiting for reply'
                return msg
            page.followers.add(request.user)
            msg = 'You successfully followed'
            return msg
        page.followers.remove(request.user)
        msg = 'You are no longer follow this page'
        return msg

    @staticmethod
    def block_pages(request):
        for page in request.user.owner_page


class PostService:
    @staticmethod
    def send_email(emails_list: list, msg: str):
        send_mail(
            os.getenv('SUBJECT', 'Innotter notification'),
            msg,
            os.getenv('EMAIL_HOST_USER'),
            emails_list,
            fail_silently=False
        )


class UploadService:
    @staticmethod
    def check_file_extension(request):
        ...