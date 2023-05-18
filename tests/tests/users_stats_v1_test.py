import pytest
from src.auth import auth_register_v2
from src.user_stats import users_stats_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_leave_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_leave_v1
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import AccessError
from src.channel import channel_messages_v2
from src.message import message_send_v1

def test_user_stats_v1_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        users_stats_v1('abc')


def test_user_stats_v1_with_channel_join_leave():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'Jake1', 'Renzella2')
    token_3 = auth_register_v2(
        'abcdee@qq.com', '123123123123', 'Jake11', 'Renzella22')

    channels_create_v2(token_1['token'], 'Channel_1', True)
    channels_create_v2(token_2['token'], 'Channel_2', True)
    channels_create_v2(token_3['token'], 'Channel_3', True)

    workspace_stats = users_stats_v1(token_1['token'])['workspace_stats']
    assert len(workspace_stats['channels_exist']) == 4
    assert len(workspace_stats['dms_exist']) == 1
    assert len(workspace_stats['messages_exist']) == 1
    assert workspace_stats['channels_exist'][-1]['num_channels_exist'] == 3
    assert workspace_stats['utilization_rate'] == 1 

def test_user_stats_v1_with_dm_create_leave():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'bb', 'bb')
    token_3 = auth_register_v2(
        'abcdee@qq.com', '123123123123', 'cc', 'cc')
    token_4 = auth_register_v2(
        'abcdeef@qq.com', '123123123123', 'dd', 'dd')
    token_5 = auth_register_v2(
        'abcdeefg@qq.com', '123123123123', 'ee', 'ee')

    dm_create_v1(token_1['token'], [])
    dm_create_v1(token_2['token'], [1])
    dm_create_v1(token_3['token'], [1,2])
    dm_create_v1(token_4['token'], [1, 2, 3])
    dm_create_v1(token_5['token'], [1, 2, 3, 4])

    workspace_stats = users_stats_v1(token_1['token'])['workspace_stats']
    print(workspace_stats)

    assert len(workspace_stats['channels_exist']) == 1
    assert len(workspace_stats['dms_exist']) == 6
    assert len(workspace_stats['messages_exist']) == 1
    assert workspace_stats['dms_exist'][-1]['num_dms_exist'] == 5
    assert workspace_stats['utilization_rate'] == 1

    dm_remove_v1(token_5['token'], 5)

    workspace_stats = users_stats_v1(token_5['token'])['workspace_stats']
 
    assert len(workspace_stats['channels_exist']) == 1
    assert len(workspace_stats['dms_exist']) == 7
    assert len(workspace_stats['messages_exist']) == 1
    assert workspace_stats['dms_exist'][-1]['num_dms_exist'] == 4
    assert workspace_stats['utilization_rate'] == 4/5

 
def test_user_stats_v1_with_message_update():
    clear_v1()
    user_1 = auth_register_v2(
        'abcsadadadaa@qq.com', '123123123123', 'Jake', 'Re')
    auth_register_v2(
        'cbajojojpjo@qq.com', '111233333333', 'God', 'jj')
    auth_register_v2(
        'cbaggggggggggggg@qq.com', '111233333333', 'pweod', 'qwerdf')
    channel_id = channels_create_v2(
        user_1["token"], "fxghh_channel", False)["channel_id"]
    message_send_v1(user_1["token"], channel_id,
                    "We are the best")["message_id"]
    channel_messages_v2(
       user_1["token"], channel_id, 0)

    workspace_stats = users_stats_v1(user_1['token'])['workspace_stats']

    assert len(workspace_stats['channels_exist']) == 2
    assert len(workspace_stats['dms_exist']) == 1
    assert len(workspace_stats['messages_exist']) == 2
    assert workspace_stats['messages_exist'][-1]['num_messages_exist'] == 1
    assert workspace_stats['utilization_rate'] == 2/3
 