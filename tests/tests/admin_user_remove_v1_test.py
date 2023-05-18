import pytest
from src.error import AccessError, InputError
from src.user_profile import user_profile_v1
from src.auth import auth_register_v2, auth_logout_v1
from src.other import clear_v1
from src.admin import admin_user_remove_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v2, channel_messages_v2
from src.message import message_send_v1


def test_admin_user_remove_v1_invalid_token():
    clear_v1()
    user = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(AccessError):
        assert admin_user_remove_v1(None, user["auth_user_id"])


def test_admin_user_remove_v1_token_is_not_owner():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(AccessError):
        assert admin_user_remove_v1(user2["token"], user1["auth_user_id"])


def test_admin_user_remove_v1_invalid_uid():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        assert admin_user_remove_v1(user1["token"], None)


def test_admin_user_remove_v1_token_is_the_only_owner():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        assert admin_user_remove_v1(user1["token"], user1["auth_user_id"])


def test_admin_user_remove_v1_is_work():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')

    channel = channels_create_v2(user1["token"], "abc", True)
    channel_join_v2(user2["token"], channel['channel_id'])
    message_send_v1(user2['token'], channel['channel_id'], 'abc')
    admin_user_remove_v1(user1["token"], user2["auth_user_id"])
    user2_details = user_profile_v1(user1["token"], user2["auth_user_id"])

    assert (
        f'{user2_details["user"]["name_first"]} {user2_details["user"]["name_last"]}') == "Removed user"

    channel_messages = channel_messages_v2(
        user1['token'], channel['channel_id'], 0)
    assert channel_messages["messages"][0]['message'] == "Removed user"


def test_admin_user_remove_v1_invalid_token_2():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    admin_user_remove_v1(user1["token"], user2["auth_user_id"])
    with pytest.raises(AccessError):
        assert auth_logout_v1(user2["token"])
