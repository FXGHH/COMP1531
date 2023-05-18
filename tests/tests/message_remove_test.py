import pytest
from src.data_store import data_store
from src.channel import channel_messages_v2, channel_invite_v2
from src.message import message_send_v1, message_remove_v1, message_senddm_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.dm import dm_create_v1
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
    # u_id = help.get_auth_user_id(user_1["token"])
    dm_id = dm_create_v1(
        user_2["token"], [user_3["auth_user_id"], user_4["auth_user_id"]])["dm_id"]
    dm_message_id_1 = message_senddm_v1(
        user_3["token"], dm_id, "Add a message")

    channel_id = channels_create_v2(
        user_1["token"], "fxghh channel", False)["channel_id"]

    channel_id_2 = channels_create_v2(
        user_2["token"], "Eric channel", False)["channel_id"]

    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "user_4": user_4, "channel_id": channel_id,
            "channel_id_2": channel_id_2, "dm_id": dm_id, "dm_message_id_1": dm_message_id_1}

################################################################################


def test_messages_invalid_token(get_token):
    with pytest.raises(AccessError):
        message_remove_v1("abc", get_token["channel_id"])


def test_messages_invalid_channel(get_token):
    with pytest.raises(InputError):
        message_remove_v1(get_token["user_1"]
                          ["token"], 101)


def test_channel_message_remove_unpermission(get_token):
    message_id = message_send_v1(get_token['user_1']["token"], get_token["channel_id"],
                                 "We are the best")["message_id"]
    channel_invite_v2(get_token['user_1']["token"],
                      get_token["channel_id"], get_token['user_3']["auth_user_id"])
    with pytest.raises(AccessError):
        message_remove_v1(get_token['user_3']
                          ["token"], message_id)


def test_channel_success_remove(get_token):
    message_id = message_send_v1(get_token['user_1']["token"], get_token["channel_id"],
                                 "We are the best")["message_id"]
    print()
    assert channel_messages_v2(
        get_token["user_1"]["token"], get_token["channel_id"], 0)["messages"][0]["message_id"] == 2
    message_remove_v1(get_token['user_1']["token"], message_id)
    assert help.message_id_is_valid_in_channel(message_id) == False
    assert channel_messages_v2(
        get_token["user_1"]["token"], get_token["channel_id"], 0) == {'end': -1, 'messages': [], 'start': 0}


def test_channel_success_remove_more_messages(get_token):
    #  add 3 message in channel_1
    message_id = message_send_v1(get_token['user_1']["token"], get_token["channel_id"],
                                 "We are the best")["message_id"]
    message_id_2 = message_send_v1(get_token['user_1']["token"], get_token["channel_id"],
                                   "a b c d e")["message_id"]
    message_id_3 = message_send_v1(get_token['user_1']["token"], get_token["channel_id"],
                                   "cccccccc")["message_id"]
    #  add 1 message in channel_2
    message_id_4 = message_send_v1(get_token['user_2']["token"], get_token["channel_id_2"],
                                   "ssw")["message_id"]
    # remove all messages in two channel
    message_remove_v1(get_token['user_2']["token"], message_id_4)
    message_remove_v1(get_token['user_1']["token"], message_id)
    message_remove_v1(get_token['user_1']["token"], message_id_3)
    message_remove_v1(get_token['user_1']["token"], message_id_2)

    assert help.message_id_is_valid_in_channel(message_id) == False
    assert channel_messages_v2(
        get_token["user_1"]["token"], get_token["channel_id"], 0) == {'end': -1, 'messages': [], 'start': 0}
    assert channel_messages_v2(
        get_token["user_2"]["token"], get_token["channel_id_2"], 0) == {'end': -1, 'messages': [], 'start': 0}


############################# dm message remove #######################
def test_dm_message_unpermission(get_token):
    with pytest.raises(AccessError):
        message_remove_v1(get_token['user_4']
                          ["token"], get_token["dm_message_id_1"]["message_id"])


def test_dm_message_success_remove_by_dm_creator(get_token):
    assert help.message_id_is_valid_in_dm(
        get_token["dm_message_id_1"]["message_id"]) == True
    message_remove_v1(get_token['user_3']
                      ["token"], get_token["dm_message_id_1"]["message_id"])
    assert help.message_id_is_valid_in_dm(
        get_token["dm_message_id_1"]["message_id"]) == False


def test_dm_message_success_remove_by_message_creator(get_token):
    assert help.message_id_is_valid_in_dm(
        get_token["dm_message_id_1"]["message_id"]) == True
    message_remove_v1(get_token['user_2']
                      ["token"], get_token["dm_message_id_1"]["message_id"])
    assert help.message_id_is_valid_in_dm(
        get_token["dm_message_id_1"]["message_id"]) == False


def test_dm_message_success_remove_by_dm_creator_2(get_token):
    message_a = message_senddm_v1(
        get_token["user_3"]["token"], get_token["dm_id"], "Add a message 2")
    message_b = message_senddm_v1(
        get_token["user_3"]["token"], get_token["dm_id"], "Add a message 3")

    assert help.message_id_is_valid_in_dm(
        get_token["dm_message_id_1"]["message_id"]) == True
    message_remove_v1(get_token['user_3']
                      ["token"], get_token["dm_message_id_1"]["message_id"])
    assert help.message_id_is_valid_in_dm(
        get_token["dm_message_id_1"]["message_id"]) == False

    assert help.message_id_is_valid_in_dm(
        message_a["message_id"]) == True
    message_remove_v1(get_token['user_3']
                      ["token"], message_a["message_id"])
    assert help.message_id_is_valid_in_dm(
        message_a["message_id"]) == False

    message_remove_v1(get_token['user_2']
                      ["token"], message_b["message_id"])
    assert help.message_id_is_valid_in_dm(
        message_b["message_id"]) == False
