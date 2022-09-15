# Generated by Django 4.1.1 on 2022-09-15 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('uuid', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField()),
                ('image', models.URLField(blank=True, null=True)),
                ('is_private', models.BooleanField(default=False)),
                ('unblock_date', models.DateTimeField(blank=True, null=True)),
                ('follow_requests', models.ManyToManyField(related_name='follow_requests_page', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(related_name='followers_page', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_page', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=180)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_post', to='page.page')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_to_post', to='page.post')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(related_name='tags_page', to='page.tag'),
        ),
    ]
