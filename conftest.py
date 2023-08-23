import uuid
import pytest

from calc.models import FurnitureInCalc, Furniture, CategoryFurniture, Calc, CalcTag, Detail


def pytest_report_header():
    """Благодарность тестеру за выполнение тестов."""
    return "Thanks for running the tests."


def pytest_report_teststatus(report):
    """Превращает неудачи в возможности."""
    if report.when == 'call' and report.failed:
        return report.outcome, 'O', 'OPPORTUNITY for improvement'


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.fixture
@pytest.mark.django_db
def db_with_1_calc(db, create_user):
    user = create_user()
    tag = CalcTag.objects.create(
        title="title_test_tag"
    ).save()
    calc = Calc.objects.create(
        designer=user,
        title="title_test",
        tags=tag
    )
    calc.save()
    Detail(
        calc=calc,
        height=100,
        width=100,
        nmb=3,
        price_material=1000
    ).save()
    category_furniture = CategoryFurniture(
        title="test_category_furniture"
    )
    category_furniture.save()
    furniture = Furniture(
        category=category_furniture,
        title="test_furniture",
        article="art",
        price=1000,
        price_retail=2000
    )
    furniture.save()
    FurnitureInCalc(
        furniture=furniture,
        calc=calc,
        nmb=3
    ).save()
    return calc



