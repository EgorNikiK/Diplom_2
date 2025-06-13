import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from helpers.data import Order
from helpers.utils import generate_random_string, generate_random_email
from helpers.utils import UserApiHelper, OrderApiHelper


@pytest.fixture
def create_user():
    user_info = UserApiHelper.register_random_user_and_return_user_info()
    yield user_info
    UserApiHelper.delete_user(user_info['token'])

@pytest.fixture
def login_info():
    email = generate_random_email(10)
    password = generate_random_string(9)
    name = generate_random_string(8)
    login_info = UserApiHelper.generate_user_login_payload(email, password, name)
    return login_info

@pytest.fixture
def create_order(create_user):
    ingredients = [Order.bun, Order.main, Order.sauce]
    order = OrderApiHelper.create_order(ingredients, create_user['token'])
    return order
