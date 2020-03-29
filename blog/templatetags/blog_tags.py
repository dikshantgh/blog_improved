# templatetags/blog_tags.py
from django import template
from django.db.models import Count

from blog.models import Post

register = template.Library()


@register.simple_tag(name='total_posts')
def total_posts():
    return Post.published.count()


@register.simple_tag(name='most_commented_posts')
def most_commented():
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:4]
