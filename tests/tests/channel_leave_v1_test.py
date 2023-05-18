import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2, auth_logout_v1
from src.channel import channel_leave_v1, channel_join_v2, channel_invite_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.help import searching_channel_with_channel_id

def test_channel_leave_v1_invalid_channel_id():
    clear_v1()
    user = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        channel_leave_v1(user['token'], 1)

def test_channel_leave_v1_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        channel_leave_v1('abc', 1)

def test_channel_leave_v1_incorrect_token_1():
    clear_v1()
    user = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user['token'], 'abc', True)
    auth_logout_v1(user['token'])
    with pytest.raises(AccessError):
        channel_leave_v1(user['token'], 1)

def test_channel_leave_v1_incorrect_token_2():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    channels_create_v2(user1['token'], 'abc', True)
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(AccessError):
        channel_leave_v1(user2['token'], 1)

def test_channel_leave_v1_is_work_1():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    channel = channels_create_v2(user1['token'], 'abc', True)
    channel_leave_v1(user1['token'], 1)
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [] and channel_details['channel_user_id'] == []

def test_channel_leave_v1_is_work_2():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')    
    channel = channels_create_v2(user1['token'], 'abc', True)
    channel_join_v2(user2['token'], channel['channel_id'])
    channel_leave_v1(user1['token'], 1)
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [] and channel_details['channel_user_id'] == [2]

def test_channel_leave_v1_is_work_3():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')    
    channel = channels_create_v2(user1['token'], 'abc', True)
    channel_invite_v2(user1['token'], channel['channel_id'], user2['auth_user_id'])
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [1] and channel_details['channel_user_id'] == [1, 2]
    channel_leave_v1(user2['token'], 1)
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [1] and channel_details['channel_user_id'] == [1]
    channel_leave_v1(user1['token'], 1)
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [] and channel_details['channel_user_id'] == []

def test_channel_leave_v1_is_work_4():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    user3 = auth_register_v2(
        'abcde@qq.com', '123123123123', 'Jake', 'Renzella')    
    channel = channels_create_v2(user1['token'], 'abc', True)
    channel_join_v2(user2['token'], channel['channel_id'])
    channel_join_v2(user3['token'], channel['channel_id'])

    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [1] and channel_details['channel_user_id'] == [1, 2, 3]
    
    channel_leave_v1(user2['token'], 1)
    
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [1] and channel_details['channel_user_id'] == [1, 3]

def test_channel_leave_v1_is_work_5():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')    
    channel = channels_create_v2(user2['token'], 'abc', True)
    channel_join_v2(user1['token'], channel['channel_id'])
    
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [2] and channel_details['channel_user_id'] == [2, 1] and channel_details['owner_permission'] == [2, 1]
    
    channel_leave_v1(user1['token'], 1)
    channel_details = searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [2] and channel_details['channel_user_id'] == [2] and channel_details['owner_permission'] == [2]