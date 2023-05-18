import pytest

from src.auth import auth_login_v2, auth_register_v2
from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store
# test login email entered does not belong to a user
def get_token_length(auth_user_id):
    store = data_store.get()
    length = 0
    for user in store['users']:
        if auth_user_id == user['auth_user_id']:
            length = len(user['token'])
    return length

def test_auth_login_v2_invalid_email_1():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_login_v2('abc@out.com','1234567')
def test_auth_login_v2_invalid_email_2():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_login_v2('abcde@outlook.com','1234567')

# test if the login password entered is correct 
def test_auth_login_v2_invalid_password_1():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_login_v2('abc@outlook.com','12345678')
def test_auth_login_v2_invalid_password_2():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_register_v2('abcd@outlook.com', '12345678', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_login_v2('abc@outlook.com','12345678')

# test if login function worked 
def test_auth_login_v2_worked_1():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')#1
    data = auth_login_v2('abc@outlook.com', '1234567') 
    length = get_token_length(data['auth_user_id'])
    assert length == 2 and data['auth_user_id'] == 1

def test_auth_login_v1_worked_2():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')#1
    auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')#2
    data = auth_login_v2('abc@outlook.com', '1234567')
    length = get_token_length(data['auth_user_id'])
    assert length == 2 and data['auth_user_id'] == 1

def test_auth_login_v1_worked_3():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')#1
    auth_login_v2('abc@outlook.com', '1234567')
    data = auth_login_v2('abc@outlook.com', '1234567')
    length = get_token_length(data['auth_user_id'])
    assert length == 3 and data['auth_user_id'] == 1