import allure
import pytest
from helpers.data import Order
from helpers.data import Responses
from helpers.utils import OrderApiHelper

@pytest.fixture
def create_order(create_user):
    token = create_user['token']
    ingredients = [Order.bun, Order.main, Order.sauce]
    order = OrderApiHelper.create_order(ingredients, token)
    return order

@pytest.fixture
def create_orders(create_user):
    token = create_user['token']
    # Создаем два заказа
    order_1 = OrderApiHelper.create_order([Order.main], token)
    order_2 = OrderApiHelper.create_order([Order.bun], token)
    return [order_1, order_2]

class TestCreateOrder:

    @allure.title('Создание заказа без авторизации.')
    def test_create_new_order_no_authorization(self):
        ingredients = [Order.bun, Order.main, Order.sauce]
        order = OrderApiHelper.create_order(ingredients)
        assert order.status_code != 200 and order.json()['success'] is not True

    @allure.title('Создание заказа с авторизацией и с валидными ингредиентами.')
    def test_create_new_order_with_authorization(self, create_order):
        assert create_order.status_code == 200 and create_order.json()['success'] is True

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

    @allure.title('Получение заказов пользователя с авторизацией.')
    def test_get_user_orders_with_authorization(self, create_orders):
        orders_list = OrderApiHelper.request_user_orders_list(create_orders[0]['token'])
        assert orders_list.status_code == 200

        created_order_ids = [order['id'] for order in create_orders]
        response_order_ids = [order['id'] for order in orders_list.json()]
        assert all(order_id in response_order_ids for order_id in created_order_ids)