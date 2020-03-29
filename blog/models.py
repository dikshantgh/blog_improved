from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


class PublishedManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='pb')


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField('Current Age', blank=True, null=True)


class Post(models.Model):
    class StatusChoice(models.TextChoices):
        published = 'pb', _('Published')
        draft = 'df', _('Draft')

    # STATUS_CHOICES = (
    #     ('draft', 'Draft'),
    #     ('published', 'Published'),
    # )
    title = models.CharField("Title of the post", max_length=50)
    tags = TaggableManager()
    total_views = models.IntegerField(default=0, blank=True, null=True)
    body = models.TextField("Post Content")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # or get_user_model()
    publish = models.DateTimeField("Publish Date", default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='title', unique_with=['title'], editable=False)
    # status = models.CharField(choices=STATUS_CHOICES, default='draft')
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.draft)
    objects = models.Manager()
    # objects = PublishedManger()
    published = PublishedManger()

    def __str__(self):
        return self.title

    def get_hits(self):     # we can achieve this using sessions too
        self.total_views += 1
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.slug,
                             self.publish.strftime('%Y'),
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             ])

    """If i use kwargs={'slug_post'} then i have to specify in views of detail view slug_kwargs_url ='slug_post'"""

    class Meta:
        # Entry.objects.latest('pub_date') in view we can use like this
        ordering = ('-publish',)
        # get_latest_by = "created"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField('Comments')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body
