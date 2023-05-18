import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v1
import src.help as help
##########################################################################################
# check when thd auth user id not in data store


def test_channel_join_check_auid_not_in_data_store():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    token_2 = ''
    channels_create_v2(token_1['token'], 'Channel_one', True)
    with pytest.raises(AccessError):
        channel_join_v2(token_2, 1)

# is private


def test_channel_join_check_is_not_pubulic():
    clear_v1()
    auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    token_2 = auth_register_v2(
        'abcasddas@qq.com', '123123123123', 'Jake', 'Renzella')
    token_3 = auth_register_v2(
        'abcas1231ddas@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(token_2['token'], 'Channel_one', False)
    with pytest.raises(AccessError):
        channel_join_v2(token_3['token'], 1)
# check id not in data store


def test_channel_join_check_chid_not_in_data_store():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        channel_join_v2(token_1['token'], 1)

# check auid already in channel


def test_channel_join_check_chid_auid_in_data_store():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(token_1['token'], 'Channel_one', True)
    with pytest.raises(InputError):
        channel_join_v2(token_1['token'], 1)

# other user no right join if not auth


def test_channel_join_check_other_in():
    clear_v1()
    auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    token_2 = auth_register_v2(
        'abcasddas@qq.com', '123123123123', 'Jake', 'Renzella')
    token_3 = auth_register_v2(
        'abcdee@qq.com', '123123123123', 'Jake11', 'Renzella22')
    channels_create_v2(token_2['token'], 'Channel_one', False)
    with pytest.raises(AccessError):
        channel_join_v2(token_3['token'], 1)

# test global owner join in private
def test_global_owner_can_join_private_channel():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    token_2 = auth_register_v2(
        'abcasddas@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(token_2['token'], 'Channel_one', False)
    channel_join_v2(token_1['token'], 1)

# test join correct
def test_channel_join_correct():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake1', 'Renzella2')
    token_3 = auth_register_v2(
        'abcdee@qq.com', '123123123123', 'Jake11', 'Renzella22')

    channels_create_v2(token_1['token'], 'Channel_one', True)
    channels_create_v2(token_2['token'], 'Channel_one', True)
    channels_create_v2(token_3['token'], 'Channel_one', False)
    channel_join_v2(token_1['token'], 2)
    channel_join_v2(token_1['token'], 3)
