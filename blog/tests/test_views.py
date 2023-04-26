from django.urls import reverse
import pytest


def test_blog_home(client):
    url = reverse('blog-about')
    response = client.get(url)
    assert response.status_code == 200
