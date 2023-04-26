from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Tag, Comment, Like
from django.contrib.auth.models import User
from .forms import CommentForm, RollbackDataForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import rollback_to
from rest_framework import generics
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    tags = post.tags.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий был добавлен!')
        return redirect('post-detail', pk=post.pk)
    return render(request, 'blog/post_detail.html', {"post": post, 'form': form})


@login_required
def rollback_view(request):
    form = RollbackDataForm()
    if request.method == 'POST':
        form = RollbackDataForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            rollback_to(date)
            messages.success(request, 'ура')
            return redirect('blog-home')
    return render(request, 'blog/rollback.html', {'form': form})


class PostDetailView(DetailView):
    model = Post


def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags__in=[tag])
    context = {
        'posts': posts,
        'tag': tag,
    }

    return render(request, 'blog/tag_posts.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.groups.get().name == 'Moderator':
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.groups.get().name == 'Moderator':
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'О клубе freakesss'})


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('post-detail', pk=post.pk)


# тут сделать обработчик чтоб принять запрос и вызвать из утилс

'''
комментарии
лайки/дизлайки
пользователи
посты
разделы
тэги
темпоральная таблица
'''