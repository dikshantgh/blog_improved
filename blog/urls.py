# blog/urls.py
"""This is the url route for blog app"""
from django.urls import path

from blog import views

app_name='blog'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/<int:year>/<int:month>/<int:day>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/update/<slug:slug>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('post/tag/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='post_list_by_tag'),  # calling list view using tag
    # path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]