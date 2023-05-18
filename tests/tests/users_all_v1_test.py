import pytest
from src.auth import auth_register_v2
from src.user_profile import users_all_v1
# from src.channel import channel_invite_v2
from src.other import clear_v1
from src.error import AccessError


def test_users_all_v1_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        users_all_v1('abc')


def test_users_all_v1_is_work_1_with_one_user():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    # print(users_all_v1(user1['token']))

    expertResult = {'users': [{'u_id': 1, 'email': 'abc@qq.com', 'name_first': 'Jake',
                              'name_last': 'Renzella', 'handle_str': 'jakerenzella'}]}
    assert users_all_v1(user1['token']) == expertResult


def test_users_all_v1_is_work_2_with_three_user():
    clear_v1()
    auth_register_v2('test1242@qq.com', 'abcd24231', 'TestF1', 'Test1234')
    auth_register_v2('test12sdfds@qq2.com',
                     'abcd234234', 'TestF2', 'Test22432')
    user1 = auth_register_v2(
        'abc11@qq.com', '123123123123', 'Jake', 'Renzella')
    # print(users_all_v1(user1['token']))
    expertResult = {'users': [{'u_id': 1, 'email': 'test1242@qq.com', 'name_first': 'TestF1', 'name_last': 'Test1234', 'handle_str': 'testf1test1234'},
                              {'u_id': 2, 'email': 'test12sdfds@qq2.com', 'name_first': 'TestF2',
                                  'name_last': 'Test22432', 'handle_str': 'testf2test22432'},
                              {'u_id': 3, 'email': 'abc11@qq.com', 'name_first': 'Jake', 'name_last': 'Renzella', 'handle_str': 'jakerenzella'}]}
    assert users_all_v1(user1['token']) == expertResult
