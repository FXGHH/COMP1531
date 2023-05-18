import pytest

from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.error import AccessError
from src.other import clear_v1
from src.data_store import data_store
import src.help as help

def get_token_length(auth_user_id):
    store = data_store.get()
    length = 0
    for user in store['users']:
        if auth_user_id == user['auth_user_id']:
            length = len(user['token'])
    return length

def test_auth_logout_v1_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        auth_logout_v1('abc')

def test_auth_logout_v1_incorrect_token():
    clear_v1()
    user = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_logout_v1(user['token'])
    with pytest.raises(AccessError):
        auth_logout_v1(user['token'])

def test_auth_logout_v1_is_work_1():
    clear_v1()
    user = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_user_id = help.get_auth_user_id(user['token'])
    length = get_token_length(auth_user_id)
    assert length == 1
    auth_logout_v1(user['token'])
    length = get_token_length(auth_user_id)
    assert length == 0
    
def test_auth_logout_v1_is_work_2():
    clear_v1()
    command1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_user_id = help.get_auth_user_id(command1['token'])
    length = get_token_length(auth_user_id)
    assert length == 1
    command2 = auth_login_v2('abc@outlook.com', '1234567')
    length = get_token_length(auth_user_id)
    assert length == 2
    auth_logout_v1(command1['token'])
    length = get_token_length(auth_user_id)
    assert length == 1
    auth_logout_v1(command2['token'])
    length = get_token_length(auth_user_id)
    assert length == 0