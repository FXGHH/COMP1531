import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1

# clear correct


def test_clear_return():
    result = clear_v1()
    assert result == {}

# clear correct


def test_clear_v1_run_when_empty_list():
    clear_v1()
    store = data_store.get()
    assert store == {'users': [], 'channels': [], 'dm': [],
                     'total_users': 0, 'total_dm': 0, 'recent_last_message_id': 0, 'standups': [],'send_later_messages': [], 'send_later_dmmessages': [],'workspace_stats':{'channels_exist':[],'dms_exist':[],'messages_exist':[] }}

# clear correct


def test_clear_v1_run_when_users_register_then_delete():
    clear_v1()
    auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    store = data_store.get()
    clear_v1()
    assert store == {'users': [], 'channels': [], 'dm': [],
                     'total_users': 0, 'total_dm': 0, 'recent_last_message_id': 0, 'standups': [],'send_later_messages': [], 'send_later_dmmessages': [],'workspace_stats':{'channels_exist':[],'dms_exist':[],'messages_exist':[] }}

# clear correct


def test_clear_v1_run_when_users_register_and_channel_create_then_delete():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(token_1['token'], 'Channel_one', True)
    store = data_store.get()
    clear_v1()
    assert store == {'users': [], 'channels': [], 'dm': [],
                     'total_users': 0, 'total_dm': 0, 'recent_last_message_id': 0, 'standups': [],'send_later_messages': [], 'send_later_dmmessages': [],'workspace_stats':{'channels_exist':[],'dms_exist':[],'messages_exist':[] }}

