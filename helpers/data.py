class Urls:

    HOME_URL = 'https://stellarburgers.nomoreparties.site/'
    USER_REGISTER_HANDLE = HOME_URL + 'api/auth/register'
    USER_LOGIN_HANDLE = HOME_URL + 'api/auth/login'
    USER_USER_HANDLE = HOME_URL + 'api/auth/user'
    ORDERS_INGREDIENTS = HOME_URL + 'api/ingredients'
    ORDERS_HANDLE = HOME_URL + 'api/orders'

class Responses:

    CODE_403_CREATE_USER_EMPTY_LOGIN = {'message': 'Email, password and name are required fields', 'success': False}
    CODE_403_CREATE_SAME_USER = {'message': 'User already exists', 'success': False}
    CODE_401_LOGIN_USER = {'message': 'email or password are incorrect', 'success': False}
    CODE_401_UPDATE_USER_NO_AUTH = {'message': 'You should be authorised', 'success': False}
    CODE_401_GET_ORDERS_NO_AUTH = {'message': 'You should be authorised', 'success': False}

class Order:
    bun = "61c0c5a71d1f82001bdaaa6d"
    main = "61c0c5a71d1f82001bdaaa71"
    sauce = "61c0c5a71d1f82001bdaaa72"