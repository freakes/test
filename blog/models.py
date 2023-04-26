from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def reviewers(self):
        queryset = self.comments.all().values_list('author__id', flat=True)
        return queryset


class Comment(models.Model):
    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Temporary(models.Model):
    StartDate = models.DateTimeField(auto_now_add=True)
    EndDate = models.DateTimeField(null=True, blank=True)
    JsonData = models.JSONField()
    action = models.CharField(max_length=20, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['StartDate']),
            models.Index(fields=['EndDate']),
        ]
