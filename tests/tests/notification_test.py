import pytest
from src.auth import auth_register_v2
from src.message import message_send_v1, message_senddm_v1, message_sendlaterdm_v1, message_sendlater_v1, message_share_v1, message_edit_v1, message_react_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.error import InputError, AccessError
from src.other import clear_v1, notifications_get_v1
import src.help as help
from src.data_store import data_store
from src.dm import dm_create_v1
import time

def test_noti_invite_correct():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'AA', 'AA')
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'BB', 'BB')
    ch1 = channels_create_v2(user1["token"], "ch1", True)
    ch2 = channels_create_v2(user2["token"], "ch2", True)
    channel_invite_v2(user1["token"], ch1["channel_id"], user2["auth_user_id"])
    channel_invite_v2(user2["token"], ch2["channel_id"], user1["auth_user_id"])

    assert notifications_get_v1(user1["token"]) == {'notifications': [{'dm_id': -1, 'channel_id': 2, 'notification_message': 'bbbb added you to ch2'}]}
    assert notifications_get_v1(user2["token"]) == {'notifications': [{'dm_id': -1, 'channel_id': 1, 'notification_message': 'aaaa added you to ch1'}]}

    dm1 = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    assert notifications_get_v1(user2["token"]) == {'notifications': [{'dm_id': 1, 'channel_id': -1, 'notification_message': 'aaaa added you to aaaa, bbbb'}, 
                                                    {'dm_id': -1, 'channel_id': 1, 'notification_message': 'aaaa added you to ch1'}]}


    message_send_v1(user2["token"], ch2["channel_id"], "@aaaa, hello ch")

    
    message_senddm_v1(user2["token"], dm1["dm_id"], "@aaaa, hello dm")
    
    now_ch = int(time.time())
    time_sent_ch = now_ch + 2
    message_sendlater_v1(user2["token"], ch2["channel_id"], "@aaaa, hello ch later", time_sent_ch)

    now_dm = int(time.time())
    time_sent_dm = now_dm + 2
    message_sendlaterdm_v1(user2["token"], dm1["dm_id"], "@aaaa, hello dm latee", time_sent_dm)
    
    message_share_v1(user2["token"],  1, "@aaaa, hello ch share", 1, -1)
    message_share_v1(user2["token"],  1, "@aaaa, hello dm share", -1, 1)

    message_edit_v1(user2["token"], 1, "@aaaa, hello ch edit")
    message_edit_v1(user2["token"], 2, "@aaaa, hello dm edit")

    message_react_v1(user1["token"], 1, 1)
    message_react_v1(user1["token"], 2, 1)

    
    assert notifications_get_v1(user1["token"]) == {'notifications': [{'dm_id': 1, 'channel_id': -1, 'notification_message': 'bbbb tagged you in aaaa, bbbb: @aaaa, hello dm edit'}, 
                                                    {'dm_id': -1, 'channel_id': 2, 'notification_message': 'bbbb tagged you in ch2: @aaaa, hello ch edit'}, 
                                                    {'dm_id': 1, 'channel_id': -1, 'notification_message': 'bbbb tagged you in aaaa, bbbb: @aaaa, hello dm shar'}, 
                                                    {'dm_id': 1, 'channel_id': -1, 'notification_message': 'bbbb tagged you in aaaa, bbbb: @aaaa, hello ch|@aaa'}, 
                                                    {'dm_id': -1, 'channel_id': 1, 'notification_message': 'bbbb tagged you in ch1: @aaaa, hello ch shar'}, 
                                                    {'dm_id': -1, 'channel_id': 1, 'notification_message': 'bbbb tagged you in ch1: @aaaa, hello ch|@aaa'}, 
                                                    {'dm_id': 1, 'channel_id': -1, 'notification_message': 'bbbb tagged you in aaaa, bbbb: @aaaa, hello dm late'}, 
                                                    {'dm_id': -1, 'channel_id': 2, 'notification_message': 'bbbb tagged you in ch2: @aaaa, hello ch late'}, 
                                                    {'dm_id': 1, 'channel_id': -1, 'notification_message': 'bbbb tagged you in aaaa, bbbb: @aaaa, hello dm'}, 
                                                    {'dm_id': -1, 'channel_id': 2, 'notification_message': 'bbbb tagged you in ch2: @aaaa, hello ch'}, 
                                                    {'dm_id': -1, 'channel_id': 2, 'notification_message': 'bbbb added you to ch2'}]}
    assert notifications_get_v1(user2["token"]) == {'notifications': [{'channel_id': -1, 'dm_id': 1, 'notification_message': 'aaaa reacted to your message in aaaa, bbbb'}, 
                                                    {'channel_id': 2, 'dm_id': -1, 'notification_message': 'aaaa reacted to your message in ch2'}, 
                                                    {'dm_id': 1, 'channel_id': -1, 'notification_message': 'aaaa added you to aaaa, bbbb'}, 
                                                    {'dm_id': -1, 'channel_id': 1, 'notification_message': 'aaaa added you to ch1'}]}