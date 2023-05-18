import pytest
from src.error import AccessError, InputError
from src.user_profile import user_profile_v1
from src.auth import auth_register_v2
from src.other import clear_v1
from src.admin import admin_userpermission_change_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v2, channel_messages_v2, channel_addowner_v1
from src.message import message_send_v1
from src.help import searching_channel_with_channel_id

def test_admin_userpermission_change_v1_invalid_token():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises (AccessError):
        assert admin_userpermission_change_v1(None, user2["auth_user_id"], 1)

def test_admin_userpermission_change_v1_token_is_not_owner():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    user3 = auth_register_v2('abcde@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises (AccessError):
        assert admin_userpermission_change_v1(user2["token"], user3["auth_user_id"], 1)

def test_admin_userpermission_change_v1_invalid_uid():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises (InputError):
        assert admin_userpermission_change_v1(user1["token"], None, 1)
    
def test_admin_userpermission_change_v1_invalid_permission_id():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises (InputError):
        assert admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], None)

def test_admin_userpermission_change_v1_is_already_permission_id():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], 1)
    with pytest.raises (InputError):
        assert admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], 1)

def test_admin_userpermission_change_v1_is_work_1():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    user3 = auth_register_v2('abcde@outlook.com', '1234567', 'Jake', 'Renzella')

    channel = channels_create_v2(user1["token"], "abc", True)
    channels_create_v2(user1["token"], "abcd", True)
    
    channel_join_v2(user2["token"], channel['channel_id'])
    channel_join_v2(user3["token"], channel['channel_id'])

    admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], 1)
    
    channel_detail = searching_channel_with_channel_id(channel['channel_id'])

    assert channel_detail['auth_user_id'] == [user1['auth_user_id']]
    assert channel_detail['owner_permission'] == [user1['auth_user_id'], user2['auth_user_id']]

    admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], 2)
    
    channel_detail = searching_channel_with_channel_id(channel['channel_id'])

    assert channel_detail['auth_user_id'] == [user1['auth_user_id']]
    assert channel_detail['owner_permission'] == [user1['auth_user_id']]

def test_admin_userpermission_change_v1_is_work_2():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    user3 = auth_register_v2('abcde@outlook.com', '1234567', 'Jake', 'Renzella')

    channel = channels_create_v2(user1["token"], "abc", True)
    channels_create_v2(user1["token"], "abcd", True)
    
    channel_join_v2(user2["token"], channel['channel_id'])
    channel_join_v2(user3["token"], channel['channel_id'])

    admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], 1)
    admin_userpermission_change_v1(user1["token"], user3['auth_user_id'], 1)
    admin_userpermission_change_v1(user2["token"], user1['auth_user_id'], 2)
    admin_userpermission_change_v1(user3["token"], user2['auth_user_id'], 2)

    channel_detail = searching_channel_with_channel_id(channel['channel_id'])

    assert channel_detail['auth_user_id'] == [user1['auth_user_id']]
    assert channel_detail['owner_permission'] == [user1['auth_user_id'], user3['auth_user_id']]
    assert channel_detail['channel_user_id'] == [user1['auth_user_id'], user2['auth_user_id'], user3['auth_user_id']]

def test_admin_userpermission_change_v1_is_work_3():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    user3 = auth_register_v2('abcde@outlook.com', '1234567', 'Jake', 'Renzella')

    channel = channels_create_v2(user1["token"], "abc", True)
    channels_create_v2(user1["token"], "abcd", True)
    
    channel_join_v2(user2["token"], channel['channel_id'])
    channel_join_v2(user3["token"], channel['channel_id'])

    channel_addowner_v1(user1["token"], channel["channel_id"], user2["auth_user_id"])

    channel_detail = searching_channel_with_channel_id(channel['channel_id'])

    assert channel_detail['auth_user_id'] == [user1['auth_user_id'], user2['auth_user_id']]
    assert channel_detail['owner_permission'] == [user1['auth_user_id'], user2['auth_user_id']]
    assert channel_detail['channel_user_id'] == [user1['auth_user_id'], user2['auth_user_id'], user3['auth_user_id']]

    admin_userpermission_change_v1(user1["token"], user2['auth_user_id'], 1)
    admin_userpermission_change_v1(user1["token"], user3['auth_user_id'], 1)
    admin_userpermission_change_v1(user2["token"], user1['auth_user_id'], 2)
    channel_detail = searching_channel_with_channel_id(channel['channel_id'])

    assert channel_detail['auth_user_id'] == [user1['auth_user_id'], user2['auth_user_id']]
    assert channel_detail['owner_permission'] == [user1['auth_user_id'], user2['auth_user_id'], user3['auth_user_id']]
    assert channel_detail['channel_user_id'] == [user1['auth_user_id'], user2['auth_user_id'], user3['auth_user_id']]   


    admin_userpermission_change_v1(user3["token"], user2['auth_user_id'], 2)
    channel_detail = searching_channel_with_channel_id(channel['channel_id'])

    assert channel_detail['auth_user_id'] == [user1['auth_user_id'], user2['auth_user_id']]
    assert channel_detail['channel_user_id'] == [user1['auth_user_id'], user2['auth_user_id'], user3['auth_user_id']]