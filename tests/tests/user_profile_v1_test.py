import pytest
from src.auth import auth_register_v2
from src.user_profile import user_profile_v1
from src.other import clear_v1
from src.error import InputError, AccessError


def test_user_profile_v1_with_invalid_token():
    with pytest.raises(AccessError):
        user_profile_v1('abc', '')


def test_user_profile_v1_with_valid_user():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        user_profile_v1(user1['token'], 10)


def test_user_profile_v1_is_ok_with_other_user():
    clear_v1()
    auth_register_v2('test1242@qq.com', 'abcd24231', 'TestF1', 'Test1234')
    auth_register_v2('test12sdfds@qq2.com',
                     'abcd234234', 'TestF2', 'Test22432')
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    expertResult = {'user': {'u_id': 2, 'email': 'test12sdfds@qq2.com',
                             'name_first': 'TestF2', 'name_last': 'Test22432', 'handle_str': 'testf2test22432'}}
    assert user_profile_v1(user1['token'], 2) == expertResult
