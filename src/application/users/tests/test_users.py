from django.urls import reverse
from application.users.models import User
from application.users.forms import UserChangePasswordForm
from django.contrib.auth.models import Permission
from http import HTTPStatus
from application.users.views import UserChangePasswordView
import pytest
from application import settings
from django.core.exceptions import ObjectDoesNotExist

# создаем администратора
@pytest.fixture()
def admin_user_1(db):
    user = User.objects.create_superuser(email='michael@gmail.com', password='0000')
    return user

# создаем пользователя
@pytest.fixture()
def user_1(db):
    user = User.objects.create_user(email='side@gmail.com', password='0000')
    return user

def test_param():
    assert UserChangePasswordView.template_name == 'users/change_password.html'
    assert UserChangePasswordView.form_class == UserChangePasswordForm
    assert UserChangePasswordView.model == User
    assert UserChangePasswordView.success_url == '/users/password/'
    assert UserChangePasswordView.is_success == False

# smoke-тест авторизированного пользователя
def test_open_page_auth_user(client, user_1):
    url = reverse('users:password')
    client.force_login(user_1)
    response = client.get(url, HTTP_HOST='0.0.0.0:8000')
    assert response.status_code == HTTPStatus.FOUND

# smoke-тест неавторизированного пользователя
def test_open_page_user(client, user_1):
    url = reverse('users:password')
    response = client.get(url, HTTP_HOST='0.0.0.0:8000')
    assert response.status_code == HTTPStatus.FOUND

# smoke-тест администратора
def test_open_page_admin(admin_client, admin_user_1):
    url = reverse('users:password')
    admin_client.force_login(admin_user_1)
    response = admin_client.get(url, HTTP_HOST='0.0.0.0:8000')
    assert response.status_code == HTTPStatus.FORBIDDEN

# smoke тест администратора + с доступом
def test_open_page_admin_add_task_users(admin_client, settings, admin_user_1):
    url = reverse('users:password')
    admin_client.force_login(admin_user_1)
    settings.ADD_TASK_USERS = (
        admin_user_1.email
    )
    response = admin_client.get(url, HTTP_HOST='0.0.0.0:8000')
    assert response.status_code == HTTPStatus.OK

# unit тест администратора на изменение пароля у пользователя
def test_admin_change_password_users(admin_client, settings, admin_user_1):
    url = reverse('users:password')
    admin_client.force_login(admin_user_1)
    settings.ADD_TASK_USERS = (
        admin_user_1.email
    )
    response = admin_client.post(url, data={'email': 'michael@gmail.com',
                                            'password': '000000', 'confirm_password': '000000'},
                                 HTTP_HOST='0.0.0.0:8000')
    assert response.status_code == HTTPStatus.FOUND



