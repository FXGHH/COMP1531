import pytest
from src.auth import auth_register_v2
from src.message import message_send_v1, message_senddm_v1
from src.channels import channels_list_v2, channels_create_v2
from src.channel import channel_messages_v2, channel_join_v2
from src.error import InputError, AccessError
from src.other import clear_v1, search_v1
import src.help as help
from src.data_store import data_store
from src.dm import dm_create_v1, dm_list_v1
# correct search
def test_search_correct():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'AA', 'AA')
    user2 = auth_register_v2('abcd@qq.com', '123123123123', 'BB', 'BB')
    channels_create_v2(user1["token"], "ch1", True)
    channels_create_v2(user2["token"], "ch1", True)
    channel_join_v2(user1['token'], 2)
    channel_join_v2(user2['token'], 1)
    message_send_v1(user1["token"], 2, "a1")
    message_send_v1(user1["token"], 2, "ab1")
    message_send_v1(user1["token"], 2, "abc1")
    message_send_v1(user1["token"], 2, "abcd1")
    message_send_v1(user1["token"], 2, "abcde1")
    message_send_v1(user1["token"], 1, "abcde2")
    message_send_v1(user1["token"], 1, "abcd2")
    message_send_v1(user1["token"], 1, "abc2")
    message_send_v1(user2["token"], 2, "2test1")
    message_send_v1(user2["token"], 2, "2test2")
    message_send_v1(user2["token"], 2, "2test3")
    dm_create_v1(user1['token'], [2])
    dm_create_v1(user2['token'], [1])
    message_senddm_v1(user1["token"], 2, "2dm_a")
    message_senddm_v1(user1["token"], 2, "2dm_ab")
    message_senddm_v1(user1["token"], 2, "2dm_abc")
    message_senddm_v1(user1["token"], 2, "2dm_abcd")
    message_senddm_v1(user1["token"], 1, "1dm_abcd")
    message_senddm_v1(user1["token"], 1, "1dm_a")

    res = search_v1(user2["token"], "t")

    assert res['messages'][0]['message'] == "2test3"
    assert res['messages'][1]['message'] == "2test2"
    assert res['messages'][2]['message'] == "2test1"


# test token error
def test_token_error():
    clear_v1()
    with pytest.raises(AccessError):
        search_v1('token', 'a')

# test query_str error
def test_query_str_error_less_1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'AA', 'AA')
    with pytest.raises(InputError):
        search_v1(user1["token"], '')

def test_query_str_error_more_than_1000():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'AA', 'AA')
    with pytest.raises(InputError):
        search_v1(user1["token"], '1' * 1111)

