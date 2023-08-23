import uuid
import pytest

from calc.models import FurnitureInCalc, Furniture, CategoryFurniture, Calc, CalcTag, Detail


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

# @pytest.fixture
# def api_client():
#     from rest_framework.test import APIClient
#     return APIClient()


# @pytest.fixture(autouse=True)
# def tasks_db(tmpdir):  # tmpdir - builtin fixture
#     """Connect to db before testing, disconnect after."""
#     # Setup : start db
#     tasks.start_tasks_db(str(tmpdir), 'tiny')
#
#     yield  # здесь происходит тестирование
#
#     # Teardown : stop db
#     tasks.stop_tasks_db()


# @pytest.fixture()
# def tasks_just_a_few():
#     """Все резюме и владельцы уникальны."""
#     return (
#         Task('Write some code', 'Brian', True),
#         Task("Code review Brian's code", 'Katie', False),
#         Task('Fix what Brian did', 'Michelle', False))

# @pytest.fixture()
# def db_with_3_tasks(tasks_db, tasks_just_a_few):
#     """Подключение БД с 3 задачами, все уникальны."""
#     for t in tasks_just_a_few:
#         tasks.add(t)

# scope='function'
# Выполняется один раз для каждой функции теста. Часть setup запускается перед каждым тестом с помощью fixture.
# Часть teardown запускается после каждого теста с использованием fixture. Это область используемая по умолчанию,
# если параметр scope не указан.
# scope='class'
# Выполняется один раз для каждого тестового класса, независимо от количества тестовых методов в классе.
# scope='module'
# Выполняется один раз для каждого модуля, независимо от того, сколько тестовых функций или методов или других фикстур
# при использовании модуля.
# scope='session'
# Выполняется один раз за сеанс. Все методы и функции тестирования, использующие фикстуру области сеанса, используют
# один вызов setup и teardown.

# @pytest.fixture(name='lue')
# def ultimate_answer_to_life_the_universe_and_everything():
#     """Возвращает окончательный ответ."""
#     return 42
# def test_everything(lue):
#     """Использует более короткое имя."""
#     assert lue == 42

### Использование tmpdir и tmpdir_factory
# Если вы тестируете что-то, что считывает, записывает или изменяет файлы, вы можете использовать tmpdir для создания
# файлов или каталогов, используемых одним тестом, и вы можете использовать tmpdir_factory, когда хотите настроить
# каталог для нескольких тестов.
# Фикстура tmpdir имеет область действия функции (function scope), и фикстура tmpdir_factory имеет область действия
# сеанса (session scope). Любой отдельный тест, которому требуется временный каталог или файл только для одного теста,
# может использовать tmpdir. Это также верно для фикстуры, которая настраивает каталог или файл, которые должны быть
# воссозданы для каждой тестовой функции.
### capsys - builtin обеспечивает две функциональные возможности: позволяет получить stdout и stderr из некоторого кода
# def test_greeting(capsys):
#     greeting('Earthling')
#     out, err = capsys.readouterr()
#     assert out == 'Hi, Earthling\n'
#     assert err == ''
# def test_capsys_disabled(capsys):
#     with capsys.disabled():
#         print('\n always print this') # всегда печатать это
#     print('normal print, usually captured') # обычная печать, обычно захваченная
### monkeypatch — это динамическая модификация класса или модуля во время выполнения
# setattr(target, name, value= < notset >, raising = True): Установить атрибут.
# delattr(target, name= < notset >, raising = True): Удалить атрибут.
# setitem(dic, name, value): Задать запись вmсловаре.
# delitem(dic, name, raising=True): Удалитьnзапись в словаре.
# setenv(name, value, prepend=None): Задать переменную окружения.
# delenv(name, raising=True): Удалите переменную окружения.
# syspath_prepend(path): Начало пути в sys.путь, который является списком папок для импорта Python.
# chdir(path): Изменить текущий рабочий каталог.
# def test_def_prefs_change_defaults(tmpdir, monkeypatch):
#     # запись в файл один раз
#     fake_home_dir = tmpdir.mkdir('home')
#     monkeypatch.setattr(cheese.os.path, 'expanduser',
#                         (lambda x: x.replace('~', str(fake_home_dir))))
#     cheese.write_default_cheese_preferences()
#     defaults_before = copy.deepcopy(cheese._default_prefs)
#     # изменение значений по умолчанию
#     monkeypatch.setitem(cheese._default_prefs, 'slicing', ['provolone'])
#     defaults_modified = cheese._default_prefs
#     # перезапись его измененными значениями по умолчанию
#     cheese.write_default_cheese_preferences()
#     # чтение и проверка
#     actual = cheese.read_cheese_preferences()
#     assert defaults_modified == actual
#     assert defaults_modified != defaults_before

# hypothesis
