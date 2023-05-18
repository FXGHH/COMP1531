import pytest
from src.auth import auth_register_v2
from src.user_profile import user_profile_v1, user_profile_setname_v1

from src.other import clear_v1
from src.error import AccessError, InputError


def test_user_profile_setname_v1_with_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        user_profile_setname_v1('abc', '', '')


def test_user_profile_setname_v1_with_invalid_first_name_1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_setname_v1(user1['token'], "", "Test")


def test_user_profile_setname_v1_with_invalid_last_name_1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_setname_v1(user1['token'], "Test", "")


def test_user_profile_setname_v1_with_invalid_first_name_2():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_setname_v1(
            user1['token'], "Test", "abcd01234567abcd01234567abcd01234567abcd01234567abcd01234567abcd01234567")


def test_user_profile_setname_v1_with_invalid_last_name_2():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_setname_v1(
            user1['token'], "abcd01234567abcd01234567abcd01234567abcd01234567abcd01234567abcd01234567", "Test")


def test_users_all_v1_is_work_2_there_user():
    clear_v1()
    user1 = auth_register_v2('test1@qq.com', '12345667', 'Jake', 'Wang')
    expertResult = {'user': {'u_id': 1, 'email': 'test1@qq.com',
                             'name_first': 'Jake', 'name_last': 'Wang', 'handle_str': 'jakewang'}}
    assert user_profile_v1(user1['token'], 1) == expertResult
    user_profile_setname_v1(user1['token'], "Lucy", "Yang")
    expertResult = {'user': {'u_id': 1, 'email': 'test1@qq.com',
                             'name_first': 'Lucy', 'name_last': 'Yang', 'handle_str': 'jakewang'}}
    assert user_profile_v1(user1['token'], 1) == expertResult
