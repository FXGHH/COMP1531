import pytest

from src.channels import channels_listall_v2, channels_create_v2
from src.auth import auth_register_v2
from src.error import AccessError
from src.other import clear_v1


def test_channels_listall_v2_1():
    clear_v1()
    user_1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user_1['token'], "qqq", True)
    assert channels_listall_v2(
        user_1['token']) == {"channels": [{'channel_id': 1, 'name': "qqq", }, ], }


def test_channels_listall_v2_2():
    clear_v1()
    user_1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user_1['token'], "qqq", False)
    channels_create_v2(user_2['token'], "aaa", True)
    assert channels_listall_v2(user_1['token']) == {"channels": [
        {'channel_id': 1, 'name': "qqq", }, {'channel_id': 2, 'name': "aaa", }], }


def test_channels_listall_v2_3():
    clear_v1()
    user_1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    user_3 = auth_register_v2(
        'abcde@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user_1['token'], "qqq", False)
    channels_create_v2(user_2['token'], "aaa", True)
    channels_create_v2(user_3['token'], "hhh", True)
    assert channels_listall_v2(user_1['token']) == {"channels": [{'channel_id': 1, 'name': "qqq", }, {
        'channel_id': 2, 'name': "aaa", }, {'channel_id': 3, 'name': "hhh", }], }


def test_channels_listall_v2_4():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v2('Eric')


def test_channels_listall_v2_5():
    clear_v1()
    user_1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    assert channels_listall_v2(user_1["token"]) == {'channels': []}
