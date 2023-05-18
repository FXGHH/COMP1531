import pytest
from src.auth import auth_register_v2
from src.user_profile import user_profile_v1, user_profile_sethandle_v1
from src.other import clear_v1
from src.error import AccessError, InputError


def test_user_profile_sethandle_v1_with_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        user_profile_sethandle_v1('abc', '')

# test length of handle_str is not between 3 and 20 characters inclusive


def test_user_profile_sethandle_v1_with_invalid_handle_1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], "1")

# test length of handle_str is not between 3 and 20 characters inclusive


def test_user_profile_sethandle_v1_with_invalid_email_2():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(
            user1['token'], "012345678901234567890123456789")

# handle_str contains characters that are not alphanumeric


def test_user_profile_sethandle_v1_with_invalid_email_3():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], "21t#@com")

# the handle is already used by another user


def test_user_profile_sethandle_v1_with_already_use_handle():
    clear_v1()
    user1 = auth_register_v2('test1@qq.com', '12345667', 'Jake', 'Wang')
    expertResult = {'user': {'u_id': 1, 'email': 'test1@qq.com',
                             'name_first': 'Jake', 'name_last': 'Wang', 'handle_str': 'jakewang'}}
    assert user_profile_v1(user1['token'], 1) == expertResult

    user2 = auth_register_v2('test2@qq.com', '12345667', 'Jake2', 'Wang2')
    expertResult = {'user': {'u_id': 2, 'email': 'test2@qq.com',
                             'name_first': 'Jake2', 'name_last': 'Wang2', 'handle_str': 'jake2wang2'}}
    assert user_profile_v1(user2['token'], 2) == expertResult

    with pytest.raises(InputError):
        user_profile_sethandle_v1(user2['token'], "jakewang")

# normal case


def test_user_profile_sethandle_v1_is_ok():
    clear_v1()
    user1 = auth_register_v2('test1@qq.com', '12345667', 'Jake', 'Wang')
    expertResult = {'user': {'u_id': 1, 'email': 'test1@qq.com',
                             'name_first': 'Jake', 'name_last': 'Wang', 'handle_str': 'jakewang'}}
    assert user_profile_v1(user1['token'], 1) == expertResult
    user_profile_sethandle_v1(user1['token'], "jakewangnew")
    expertResult = {'user': {'u_id': 1, 'email': 'test1@qq.com',
                             'name_first': 'Jake', 'name_last': 'Wang', 'handle_str': 'jakewangnew'}}
    assert user_profile_v1(user1['token'], 1) == expertResult
