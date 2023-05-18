import pytest
from src.data_store import data_store
from src.channel import channel_messages_v2, channel_invite_v2
from src.message import message_send_v1, message_remove_v1, message_senddm_v1, message_share_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
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


def test_messages_share_invalid_token(get_token):
    with pytest.raises(AccessError):
        message_share_v1("abc", get_token["channel_message_id_1"],
                         "share a message", get_token["channel_id"], -1)


def test_messages_share_invalid_input_id_1(get_token):
    with pytest.raises(InputError):
        message_share_v1(get_token["user_1"]["token"], get_token["channel_message_id_1"],
                         "share a message", -1, -1)


def test_messages_share_invalid_input_id_2(get_token):
    with pytest.raises(InputError):
        message_share_v1(get_token["user_1"]["token"], get_token["channel_message_id_1"],
                         "share a message", get_token["channel_id"], get_token["dm_id"])


def test_messages_share_invalid_message_id(get_token):
    with pytest.raises(InputError):
        message_share_v1(get_token["user_1"]["token"], 131,
                         "share a message", get_token["channel_id"], -1)


def test_messages_share_invalid_message_length(get_token):
    string = ""
    for i in range(0, 1001):
        string += str(i)
    with pytest.raises(InputError):
        message_share_v1(get_token["user_1"]["token"], get_token["channel_message_id_1"],
                         string, get_token["channel_id"], -1)


def test_messages_share_not_authorised_with_og_message_channel(get_token):
    with pytest.raises(InputError):
        message_share_v1(get_token["user_2"]["token"], get_token["channel_message_id_1"],
                         "share a message", get_token["channel_id"], -1)


def test_messages_share_not_authorised_with_og_message_dm(get_token):
    with pytest.raises(InputError):
        message_share_v1(get_token["user_1"]["token"], get_token["dm_message_id_1"],
                         "share a message", -1, get_token["dm_id"])


def test_messages_share_not_join_channel(get_token):
    with pytest.raises(AccessError):
        message_share_v1(get_token["user_2"]["token"], get_token["dm_message_id_1"],
                         "share a message", get_token["channel_id"], -1)


def test_messages_share_not_join_dm(get_token):
    with pytest.raises(AccessError):
        message_share_v1(get_token["user_1"]["token"], get_token["channel_message_id_1"],
                         "share a message", -1, get_token["dm_id"])


####################### share success #######################
def test_messages_share_success_channel_to_channel(get_token):
    channel_id_3 = channels_create_v2(
        get_token["user_1"]["token"], "fxghh_new_channel", False)["channel_id"]

    message_share_v1(get_token["user_1"]["token"], get_token["channel_message_id_1"],
                     "share a message", channel_id_3, -1)
    message_detail = channel_messages_v2(
        get_token['user_1']["token"], channel_id_3, 0)
    assert message_detail["messages"][0]["message"] == "Send message 1|share a message"


def test_messages_share_success_channel_to_dm(get_token):
    channel_message_id_2 = message_send_v1(
        get_token["user_2"]["token"], get_token["channel_id_2"], "Send message 1")["message_id"]

    message_share_v1(get_token["user_2"]["token"], channel_message_id_2,
                     "share a message", -1, get_token["dm_id"])

    message_detail = dm_messages_v1(
        get_token['user_2']["token"], get_token["dm_id"], 0)
    assert message_detail['messages'][0]["message"] == "Send message 1|share a message"


def test_messages_share_success_dm_to_dm(get_token):
    message_share_v1(get_token["user_2"]["token"], get_token["dm_message_id_1"],
                     "share a message", -1, get_token["dm_id_2"])
    message_detail = dm_messages_v1(
        get_token['user_2']["token"], get_token["dm_id_2"], 0)
    assert message_detail['messages'][0]["message"] == "Send message 1|share a message"


def test_messages_share_success_dm_to_channel(get_token):
    message_share_v1(get_token["user_2"]["token"], get_token["dm_message_id_1"],
                     "share a message", get_token["channel_id_2"], -1)
    message_detail = channel_messages_v2(
        get_token['user_2']["token"], get_token["channel_id_2"], 0)
    assert message_detail['messages'][0]["message"] == "Send message 1|share a message"
