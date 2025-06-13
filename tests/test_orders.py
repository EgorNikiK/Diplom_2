import allure
import pytest
from helpers.data import Order
from helpers.data import Responses
from helpers.utils import OrderApiHelper


class TestCreateOrder:

    @allure.title('Создание заказа без авторизации.')
    def test_create_new_order_no_authorization(self):
        ingredients = [Order.bun, Order.main, Order.sauce]
        order = OrderApiHelper.create_order(ingredients)
        assert order.status_code != 200 and order.json()['success'] != True

    @allure.title('Создание заказа с авторизацией и с валидными ингредиентами.')
    def test_create_new_order_with_authorization(self, create_order):
        assert create_order.status_code == 200 and create_order.json()['success'] == True

    @allure.title('Создание заказа с авторизацией без ингредиентов/с невалидными ингредиентами.')
    @pytest.mark.parametrize("ingredients, code", [([], 400), (["invalid"], 500)])
    def test_create_new_order_invalid_ingredients(self, create_user, ingredients, code):
        order = OrderApiHelper.create_order(ingredients, create_user['token'])
        assert order.status_code == code


class TestGetOrder:

    @allure.title('Получение заказов пользователя без авторизации.')
    def test_get_user_orders_with_authorization(self, create_order):
        orders = OrderApiHelper.request_user_orders_list()
        assert orders.status_code == 401 and orders.json() == Responses.CODE_401_GET_ORDERS_NO_AUTH

    @allure.title('Получение заказов пользователя c авторизацией.')
    def test_get_user_orders_with_authorization(self, create_user):
        token = create_user['token']

        order_1 = OrderApiHelper.create_order(Order.main, token)
        assert order_1.status_code == 200
        order_2 = OrderApiHelper.create_order(Order.bun, token)
        assert order_2.status_code == 200

        orders_list = OrderApiHelper.request_user_orders_list(token)
        assert orders_list.status_code == 200