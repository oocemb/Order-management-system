import os

from django.urls import reverse


def test_paginated_posts(db_with_posts, client):
    url = reverse('posts_list')
    post_per_page = os.getenv("POST_PER_PAGE", 3)
    response = client.get(url)
    assert "is_paginated" in response.context
    assert response.context["is_paginated"]
    assert len(response.context["posts"]) == int(post_per_page)
