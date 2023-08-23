import pytest

from blog.models import Post


@pytest.fixture
@pytest.mark.django_db
def db_with_posts(db):
    # Create 15 post for pagination tests
    number_of_post = 15

    for post_id in range(1, number_of_post):
        Post.objects.create(
            title=f'Dominique {post_id}',
            body=f'Surname {post_id}',
        )
