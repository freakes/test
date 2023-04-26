from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<slug:slug>', views.posts_by_tag, name='tag-posts'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('rollback/', views.rollback_view, name='rollback'),
    path('resttest/', views.PostList.as_view()),
]

'''
как должна работать и быть реализована функция отката изменений - применение всех измененний ДО даты которую передали в функцию
связывающие таблицы
роли - через auth group
'''