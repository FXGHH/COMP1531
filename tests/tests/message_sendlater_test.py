import pytest
from src.data_store import data_store
from src.channel import channel_messages_v2, channel_invite_v2
from src.message import message_send_v1, message_remove_v1, message_senddm_v1, message_sendlater_v1
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


def test_messages_snedlater_invalid_token(get_token):
    now = int(time.time())
    time_sent = now + 2
    with pytest.raises(AccessError):
        message_sendlater_v1("abc", get_token["channel_id"],
                             "future messsage", time_sent)


def test_messages_snedlater_invalid_message_length(get_token):
    now = int(time.time())
    time_sent = now + 2
    string = ""
    for i in range(0, 1001):
        string += str(i)
    with pytest.raises(InputError):
        message_sendlater_v1(get_token["user_1"]["token"], get_token["channel_id"],
                             string, time_sent)
    with pytest.raises(InputError):
        message_sendlater_v1(get_token["user_1"]["token"], get_token["channel_id"],
                             '', time_sent)


def test_messages_snedlater_invalid_channel_id(get_token):
    now = int(time.time())
    time_sent = now + 2
    with pytest.raises(InputError):
        message_sendlater_v1(get_token["user_1"]["token"], -1,
                             "future messsage", time_sent)


def test_messages_snedlater_invalid_time_sent(get_token):
    now = int(time.time())
    time_sent = now - 1
    with pytest.raises(InputError):
        message_sendlater_v1(get_token["user_1"]["token"], get_token["channel_id"],
                             "future messsage", time_sent)


def test_messages_snedlater_invalid_time_input(get_token):
    now = int(time.time())
    time_sent = now + 2
    with pytest.raises(AccessError):
        message_sendlater_v1(get_token["user_2"]["token"], get_token["channel_id"],
                             "future messsage", time_sent)


def test_messages_snedlater_success_send(get_token):
    now = int(time.time())
    time_sent = now + 2
    later_message_id = message_sendlater_v1(get_token["user_1"]["token"], get_token["channel_id"],
                                            "future messsage", time_sent)
    found_channel_org = help.searching_channel_with_channel_id(
        get_token["channel_id"])
    assert later_message_id["message_id"] == 3
    assert len(found_channel_org["message"]) == 1
    assert found_channel_org["message"][0]["message"] == "Send message 1"
    time.sleep(3)
    found_channel_later = help.searching_channel_with_channel_id(
        get_token["channel_id"])
    assert len(found_channel_later["message"]) == 2
    assert found_channel_later["message"][0]["message"] == "future messsage"
    assert found_channel_later["message"][1]["message"] == "Send message 1"
