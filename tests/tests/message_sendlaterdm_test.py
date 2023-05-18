from ast import Store
import pytest
from src.data_store import data_store
from src.channel import channel_messages_v2, channel_invite_v2
from src.message import message_send_v1, message_remove_v1, message_senddm_v1, message_sendlaterdm_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
import time
import src.help as help


@pytest.fixture
def get_token():
    clear_v1()
    user_1 = auth_register_v2(
        'abcsadadadaa@qq.com', '123123123123', 'Jake', 'Re')
    user_2 = auth_register_v2(
        'cbajojojpjo@qq.com', '111233333333', 'God', 'jj')
    user_3 = auth_register_v2(
        'cbaggggggggggggg@qq.com', '111233333333', 'pweod', 'qwerdf')
    user_4 = auth_register_v2(
        'jlj990011sjcja@qq.com', '48370908ss', 'python', 'Java')
    dm_id = dm_create_v1(
        user_2["token"], [user_3["auth_user_id"], user_4["auth_user_id"]])["dm_id"]
    dm_id_2 = dm_create_v1(
        user_3["token"], [user_2["auth_user_id"]])["dm_id"]

    dm_message_id_1 = message_senddm_v1(
        user_3["token"], dm_id, "Send message 1")["message_id"]
    channel_id = channels_create_v2(
        user_1["token"], "fxghh channel", False)["channel_id"]

    channel_id_2 = channels_create_v2(
        user_2["token"], "Eric channel", False)["channel_id"]

    channel_message_id_1 = message_send_v1(
        user_1["token"], channel_id, "Send message 1")["message_id"]

    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "user_4": user_4, "channel_id": channel_id,
            "channel_message_id_1": channel_message_id_1, "channel_id_2": channel_id_2, "dm_id": dm_id, "dm_id_2": dm_id_2, "dm_message_id_1": dm_message_id_1}


def test_messages_snedlaterdm_invalid_token(get_token):
    now = int(time.time())
    time_sent = now + 2
    with pytest.raises(AccessError):
        message_sendlaterdm_v1("abc", get_token["dm_id"],
                               "future messsage", time_sent)


def test_messages_snedlaterdm_invalid_message_length(get_token):
    now = int(time.time())
    time_sent = now + 2
    string = ""
    for i in range(0, 1001):
        string += str(i)
    with pytest.raises(InputError):
        message_sendlaterdm_v1(get_token["user_1"]["token"], get_token["dm_id"],
                               string, time_sent)
    with pytest.raises(InputError):
        message_sendlaterdm_v1(get_token["user_1"]["token"], get_token["dm_id"],
                               '', time_sent)


def test_messages_snedlaterdm_invalid_dm_id(get_token):
    now = int(time.time())
    time_sent = now + 2
    with pytest.raises(InputError):
        message_sendlaterdm_v1(get_token["user_2"]["token"], -1,
                               "future messsage", time_sent)


def test_messages_snedlaterdm_invalid_time_sent(get_token):
    now = int(time.time())
    time_sent = now - 1
    with pytest.raises(InputError):
        message_sendlaterdm_v1(get_token["user_2"]["token"], get_token["dm_id"],
                               "future messsage", time_sent)


def test_messages_snedlaterdm_not_member(get_token):
    now = int(time.time())
    time_sent = now + 2
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(get_token["user_1"]["token"], get_token["dm_id"],
                               "future messsage", time_sent)


def test_messages_snedlaterdm_success_send(get_token):
    store = data_store.get()
    now = int(time.time())
    time_sent = now + 2
    later_message_id = message_sendlaterdm_v1(get_token["user_2"]["token"], get_token["dm_id"],
                                              "future messsage", time_sent)["message_id"]
    assert store["send_later_dmmessages"] != []
    assert len(store["send_later_dmmessages"]) == 1
    found_dm_org = help.searching_dm_with_dm_id(
        get_token["dm_id"])
    assert later_message_id == 3
    assert len(found_dm_org["dm_messages"]) == 1
    assert found_dm_org["dm_messages"][0]["message"] == "Send message 1"
    time.sleep(3)
    found_dm_later = help.searching_dm_with_dm_id(
        get_token["dm_id"])
    assert len(found_dm_later["dm_messages"]) == 2
    assert found_dm_later["dm_messages"][0]["message"] == "future messsage"
    assert found_dm_later["dm_messages"][1]["message"] == "Send message 1"
    new_dm_mess_id = message_senddm_v1(get_token["user_2"]["token"], get_token["dm_id"],
                                       "future messsage")["message_id"]
    assert new_dm_mess_id == 4
    assert store["send_later_dmmessages"] == []
