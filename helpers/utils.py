import allure
import requests
import random
import string
from helpers.data import Urls


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_random_email(length):
    return generate_random_string(length) + '@test.com'

class UserApiHelper:

    @staticmethod
    def generate_user_login_payload(email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return payload

    @staticmethod
    @allure.step('Регистрация пользователя с помощью email и пароля.')
    def register_user(payload):
        return requests.post(Urls.USER_REGISTER_HANDLE, data=payload)

    @staticmethod
    @allure.step('Регистрация random пользователя и получение его email и пароля.')
    def register_random_user_and_return_user_info():
        user_info = {}

        email = generate_random_email(10)
        password = generate_random_string(10)
        name = generate_random_string(10)

        response = UserApiHelper.register_user(UserApiHelper.generate_user_login_payload(email, password, name))

        if response.status_code == 200:
            user_info['email'] = email
            user_info['password'] = password
            user_info['name'] = name
            user_info['token'] = response.json()['accessToken']

        return user_info

    @staticmethod
    @allure.step('Авторизация пользователя с помощью email и пароля.')
    def login_user(email: str, password: str):
        return requests.post(Urls.USER_LOGIN_HANDLE, json={"email": email, "password": password})

    @staticmethod
    @allure.step('Изменение данных пользователя.')
    def update_user(params, token):
        return requests.patch(Urls.USER_USER_HANDLE, json=params, headers={"Authorization": f"{token}"})

    @staticmethod
    @allure.step('Удаление пользователя.')
    def delete_user(token):
        return requests.delete(Urls.USER_USER_HANDLE, headers={"Authorization": f"{token}"})

class OrderApiHelper:

    @staticmethod
    @allure.step('Создание нового заказа.')
    def create_order(ingredients, token = ''):
        return requests.post(Urls.ORDERS_HANDLE, json={"ingredients": ingredients}, headers={"Authorization": f"{token}"})

    @staticmethod
    @allure.step('Получение списка заказов.')
    def request_user_orders_list(token = ''):
        return requests.get(Urls.ORDERS_HANDLE, headers={"Authorization": f"{token}"})