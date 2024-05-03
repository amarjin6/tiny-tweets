import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from page.models import Page, Post, Tag
from user.tests.factories import UserFactory


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('pystr')


@register
class PageFactory(DjangoModelFactory):
    class Meta:
        model = Page

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    title = factory.Faker('bs')
    uuid = factory.Faker('pyint', min_value=0, max_value=100)
    owner = factory.SubFactory(UserFactory)
    image = factory.Faker("image_url")
    description = factory.Faker('pyint')

    @factory.post_generation
    def followers(self, create, extracted):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                self.followers.add(UserFactory())

    @factory.post_generation
    def follow_requests(self, create, extracted):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                self.follow_requests.add(UserFactory())


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    page = factory.SubFactory(PageFactory)
    content = factory.Faker('sentence')
    owner = factory.SubFactory(UserFactory)
