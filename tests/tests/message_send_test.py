import pytest
from src.data_store import data_store
from src.channel import channel_messages_v2
from src.message import message_send_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
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
    return {"user_1": user_1, "user_2": user_2, "user_3": user_3}

# out the range of messages index


def test_messages_success_send(get_token):
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    message_send_v1(get_token['user_1']["token"], channel_id,
                    "We are the best")["message_id"]
    message_detail = channel_messages_v2(
        get_token['user_1']["token"], channel_id, 0)
    assert message_detail["start"] == 0
    assert message_detail["end"] == -1
    assert message_detail["messages"][0]["message_id"] == 1
    assert message_detail["messages"][0]["u_id"] == 1
    assert message_detail["messages"][0]["message"] == "We are the best"


def test_messages_invalid_token(get_token):
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    with pytest.raises(AccessError):
        message_send_v1("abc", channel_id,
                        "We are the best")["message_id"]


def test_messages_invalid_channel(get_token):
    channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    with pytest.raises(InputError):
        message_send_v1(get_token["user_1"]["token"], 101, "We are the best")


def test_messages_invalid_access(get_token):
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    with pytest.raises(AccessError):
        message_send_v1(get_token["user_2"]["token"],
                        channel_id, "We are the best")


def test_messages_invalid_message_length_less_1(get_token):
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    with pytest.raises(InputError):
        message_send_v1(get_token["user_1"]["token"],
                        channel_id, "")


def test_messages_invalid_message_length_over_1000(get_token):
    string = ""
    for i in range(0, 1001):
        string += str(i)
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    with pytest.raises(InputError):
        message_send_v1(get_token["user_1"]["token"],
                        channel_id, string)


def test_messages_success_send_more_channel(get_token):
    channels_create_v2(
        get_token['user_3']["token"], "fxghh_channel", False)["channel_id"]
    channels_create_v2(
        get_token['user_2']["token"], "fxghh_channel", False)["channel_id"]
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    message_send_v1(get_token['user_1']["token"], channel_id,
                    "We are the best")
    message_detail = channel_messages_v2(
        get_token['user_1']["token"], channel_id, 0)
    assert message_detail["start"] == 0
    assert message_detail["end"] == -1
    assert message_detail["messages"][0]["message_id"] == 1
    assert message_detail["messages"][0]["u_id"] == 1
    assert message_detail["messages"][0]["message"] == "We are the best"


def test_messages_empty_channel_list(get_token):
    channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", False)["channel_id"]
    with pytest.raises(InputError):
        message_send_v1(get_token["user_1"]["token"], 101, "We are the best")
