import allure
import pytest
import requests
from helpers.data import Responses
from helpers.data import Urls
from helpers.utils import generate_random_string, generate_random_email
from helpers.utils import UserApiHelper


class TestLoginUser:

    @allure.title('Авторизация зарегистрированного пользователя с помощью email и пароля.')
    def test_login_user(self, create_user):
        response = UserApiHelper.login_user(create_user['email'], create_user['password'])
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Авторизация пользователя с неверным логином/паролем.')
    @pytest.mark.parametrize("email, password", [(True, False),
                                                 (False, True)])
    def test_login_user_incorrect_login_password(self, create_user, email, password):
        email = create_user['email'] if email== True else 'test_email@m.com'
        password = create_user['password'] if password == True else 'test_password'
        response = UserApiHelper.login_user(email, password)
        assert response.status_code == 401 and response.json() == Responses.CODE_401_LOGIN_USER

class TestCreateUser:

    @allure.title('Регистрация нового пользователя.')
    def test_create_new_user(self, login_info):

        response = UserApiHelper.register_user(login_info)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Регистрация двух одинаковых пользователей.')
    def test_create_two_same_users(self, login_info):

        UserApiHelper.register_user(login_info)
        response = UserApiHelper.register_user(login_info)
        assert response.status_code == 403 and response.json() == Responses.CODE_403_CREATE_SAME_USER

    @allure.title('Регистрация пользователя без логина/пароля.')
    @pytest.mark.parametrize("email, password, name", [('', generate_random_string(10), generate_random_string(10)),
                                                       (generate_random_email(10), '', generate_random_string(10)),
                                                       (generate_random_email(10), generate_random_string(10), '')])
    def test_create_user_no_login_no_password_no_name(self, email, password, name):

        response = UserApiHelper.register_user(UserApiHelper.generate_user_login_payload(email, password, name))
        assert response.status_code == 403 and response.json() == Responses.CODE_403_CREATE_USER_EMPTY_LOGIN

class TestUpdateUser:

    @allure.title('Изменение данных пользователя без авторизации.')
    @pytest.mark.parametrize("param", [({"email": "test131313@mail.tu"}),
                                       ({"password": "test131313"}),
                                       ({"name": "test131313"})])
    def test_update_no_authorized_user(self, create_user, param):
        response = requests.patch(Urls.USER_USER_HANDLE, json=param)
        assert response.status_code == 401 and response.json() == Responses.CODE_401_UPDATE_USER_NO_AUTH

    @allure.title('Изменение данных пользователя c авторизацией.')
    @pytest.mark.parametrize("param", [({"email": "test333336@mail.tu"}),
                                       ({"password": "test333335"}),
                                       ({"name": "test333335"})])
    def test_update_authorized_user(self, create_user, param):
        response = requests.patch(Urls.USER_USER_HANDLE, json=param, headers={"Authorization": f"{create_user['token']}"})
        assert response.status_code == 200 and response.json()['success'] == True
