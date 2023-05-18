import pytest
from src.auth import auth_register_v2
from src.channels import channels_list_v2, channels_create_v2
# from src.channel import channel_invite_v2
from src.other import clear_v1
from src.error import AccessError
def test_channels_list_v2_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        channels_list_v2('abc')
def test_channels_list_v2_is_work_1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    assert channels_list_v2(user1['token']) == {"channels": [{'channel_id': 1,'name': "abc",},],}
def test_channels_list_v2_is_work_2():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], "abc", True)
    channels_create_v2(user1['token'], "def", True)
    assert channels_list_v2(user1['token']) == {"channels": [{'channel_id': 1,'name': "abc",}, {'channel_id': 2,'name': "def",},],}   
def test_channels_list_v2_is_work_3():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], "abc", True)
    channels_create_v2(user2['token'], "abc", True)
    channels_create_v2(user2['token'], "def", False)
    assert channels_list_v2(user2['token']) == {"channels": [{'channel_id': 2,'name': "abc",}, {'channel_id': 3,'name': "def",},],}
def test_channels_list_v2_is_work_4():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], "abc", True)
    assert channels_list_v2(user1['token']) == {"channels": [{'channel_id': 1,'name': "abc",},],}
    channels_create_v2(user1['token'], "abc", True)
    assert channels_list_v2(user1['token']) == {"channels": [{'channel_id': 1,'name': "abc",}, {'channel_id': 2,'name': "abc",},],}
    channels_create_v2(user2['token'], "def", False)
    assert channels_list_v2(user2['token']) == {"channels": [{'channel_id': 3,'name': "def",},],}
def test_channels_list_v2_is_work_5():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], "abc", True)
    channels_create_v2(user2['token'], "abc", True)
    assert channels_list_v2(user1['token']) == {"channels": [{'channel_id': 1,'name': "abc",},],}
    channels_create_v2(user1['token'], "def", False)
    channels_create_v2(user2['token'], "def", False)
    assert channels_list_v2(user2['token']) == {"channels": [{'channel_id': 2,'name': "abc",}, {'channel_id': 4,'name': "def",},],}
def test_channels_list_v2_is_work_6():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    assert channels_list_v2(user1['token']) == {"channels": [],}
# def test_channels_list_v2_it1failed_1():
#     clear_v1()
#     user1 = auth_register_v2('sheriff.woody@andysroom.com', 'qazwsx!!', 'sheriff', 'woody')
#     user2 = auth_register_v2('zerg.thedestroyer@zergworld.com', '!!qazwsx', 'lord', 'zerg')
#     channels_create_v2(user1['token'], "andy", False)
#     channel_invite_v2(user1['token'], 1, 2)  
#     assert channels_list_v2(user2['token']) == {"channels": [{'channel_id': 1,'name': "andy",},],}
# def test_channels_list_v2_it1failed_2():
#     clear_v1()
#     user1 = auth_register_v2('sheriff.woody@andysroom.com', 'qazwsx!!', 'sheriff', 'woody')
#     user2 = auth_register_v2('zerg.thedestroyer@zergworld.com', '!!qazwsx', 'lord', 'zerg')
#     channels_create_v2(user1['token'], "andy", True)
#     channel_invite_v2(user1['token'], 1, 2)  
#     assert channels_list_v2(user2['token']) == {"channels": [{'channel_id': 1,'name': "andy",},],}