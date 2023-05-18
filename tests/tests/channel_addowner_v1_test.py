import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2, auth_logout_v1
from src.channel import channel_addowner_v1, channel_join_v2, channel_invite_v2
from src.channels import channels_create_v2
from src.other import clear_v1
import src.help as help

def test_channel_addowner_v1_invalid_token_1(): # token invalid
    clear_v1()
    with pytest.raises(AccessError):
        channel_addowner_v1('abc', 1, 1)

def test_channel_addowner_v1_invalid_token_2(): # token invalid
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    channel_join_v2(user2['token'], 1)
    auth_logout_v1(user1['token'])
    with pytest.raises(AccessError):
        channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])

def test_channel_addowner_v1_incorrect_token_1(): # token no permission
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    channels_create_v2(user1['token'], 'abc', True)
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella') 
    channel_join_v2(user2['token'], 1)
    with pytest.raises(AccessError):
        channel_addowner_v1(user2['token'], 1, user2['auth_user_id'])

def test_channel_addowner_v1_incorrect_token_2(): # token no permission and uid invalid
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')  
    channels_create_v2(user1['token'], 'abc', True)
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella') 
    channel_join_v2(user2['token'], 1)
    user3 = auth_register_v2(
        'abcde@qq.com', '123123123123', 'Jake', 'Renzella') 
    with pytest.raises(AccessError):
        channel_addowner_v1(user2['token'], 1, user3['auth_user_id'])

def test_channel_addowner_v1_invalid_channel_id():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])

def test_channel_addowner_v1_invalid_uid():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    with pytest.raises(InputError):
        channel_addowner_v1(user1['token'], 1, 2)

def test_channel_addowner_v1_incorrect_uid():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])

def test_channel_addowner_v1_already_owner_1():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    with pytest.raises(InputError):
        channel_addowner_v1(user1['token'], 1, user1['auth_user_id'])

def test_channel_addowner_v1_already_owner_2():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    channel_join_v2(user2['token'], 1)
    channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])
    with pytest.raises(InputError):
        channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])

def test_channel_addowner_v1_is_work_1_public_channel():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channel = channels_create_v2(user1['token'], 'abc', True)
    channel_invite_v2(user1['token'], 1, user2['auth_user_id'])
    channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])
    channel_details = help.searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [user1['auth_user_id'], user2['auth_user_id']]

def test_channel_addowner_v1_is_work_1_private_channel():
    clear_v1()
    user1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    user2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake', 'Renzella')
    channel = channels_create_v2(user1['token'], 'abc', False)
    channel_invite_v2(user1['token'], 1, user2['auth_user_id'])
    channel_addowner_v1(user1['token'], 1, user2['auth_user_id'])
    channel_details = help.searching_channel_with_channel_id(channel['channel_id'])
    assert channel_details['auth_user_id'] == [user1['auth_user_id'], user2['auth_user_id']]
