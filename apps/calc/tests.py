import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from calc.utils import (
    current_furniture_in_calc_and_main_calc_info,
    current_details_in_calc_and_main_calc_info,
    validate_calc_id,
)
from calc.models import Calc, Comment
from calc.forms import CommentForm


def test_connection_with_reverse(client):
    url = reverse('calc_list')
    response = client.get(url)
    assert response.status_code == 200


def test_unauthorized(client):
    url = reverse('admin:index')
    response = client.get(url)
    assert response.status_code == 302


def test_superuser_view(admin_client):
    url = reverse('admin:index')
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1


def test_calc_create(db_with_1_calc):
    assert Calc.objects.count() == 1


def test_leave_comment(db_with_1_calc, client):
    calc = db_with_1_calc
    url = reverse('leave_comment', kwargs={"calc_id": calc.id})
    form_data = {'title': 'test_title', "text": "my_test_text"}
    form = CommentForm(data=form_data)
    client.post(url, data=form_data)
    if not form.is_valid():
        err = form.errors
    assert form.is_valid()
    assert Comment.objects.count() == 1


def test_calc_details_info(db_with_1_calc):
    calc = db_with_1_calc
    details = current_details_in_calc_and_main_calc_info(calc_id=calc.id)
    assert details["details_total_nmb"] == 3
    assert details["total_calc_price"] == 3000
    assert len(details["details"]) == 1
    assert details["details"][0]["id"] == 1
    assert details["details"][0]["height"] == 100


def test_calc_furniture_info(db_with_1_calc):
    calc = db_with_1_calc
    furniture = current_furniture_in_calc_and_main_calc_info(calc_id=calc.id)
    assert furniture["furniture_total_nmb"] == 3
    assert furniture["total_calc_price"] == 6000
    assert len(furniture["furniture"]) == 1
    assert furniture["furniture"][0]["id"] == 1
    assert furniture["furniture"][0]["furniture_id"] == 1


@pytest.mark.django_db
def test_auth_view(client, django_user_model, test_password):
    user = django_user_model.objects.create_user(
        username='someone',
        password=test_password
    )
    url = reverse('adding_calc')
    response = client.get(url)
    assert response.status_code == 302
    client.login(
        username=user.username, password=test_password
    )
    response = client.get(url)
    assert response.status_code == 200


bad_calc_id_params = [-1, 0, 1.1, "str"]


@pytest.mark.smoke
@pytest.mark.parametrize("calc_id", bad_calc_id_params)
@pytest.mark.django_db
def test_validate_calc_id(calc_id):
    with pytest.raises(ValueError):
        validate_calc_id(calc_id)


@pytest.mark.smoke
@pytest.mark.django_db
def test_current_furniture_bad_id():
    current_furniture_in_calc_and_main_calc_info(1)
