from os import access
import pytest
from src.message import message_send_v1
from src.data_store import data_store
from src.channel import channel_messages_v2
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


# invalid Channel ID
def test_channel_messages_v2_no_channel_found(get_token):
    with pytest.raises(InputError):
        channel_messages_v2(get_token["user_1"]["token"], 101, 0)


# invalid token
def test_channel_messages_v2_invild_token(get_token):
    channel_id = channels_create_v2(
        get_token["user_2"]["token"], "ioi", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_messages_v2('abc', channel_id, 0)


# out the range of messages index
def test_channel_messages_v2_out_range_messages(get_token):
    channel_id = channels_create_v2(
        get_token["user_2"]["token"], "ioi", True)["channel_id"]
    message_send_v1(get_token['user_2']["token"], channel_id,
                    "We are the best")
    with pytest.raises(InputError):
        channel_messages_v2(get_token["user_2"]
                            ["token"], channel_id, 100)  # user_2


# no message in channel
def test_channel_messages_v2_no_message(get_token):
    channel_id = channels_create_v2(
        get_token["user_2"]["token"], "ioi", True)["channel_id"]
    assert channel_messages_v2(get_token["user_2"]["token"], channel_id, 0) == {
        "messages": [],
        "start": 0,
        "end": -1
    }


# Can't access the channel
def test_channel_messages_v2_invild_access(get_token):
    channel_id = channels_create_v2(
        get_token["user_1"]["token"], "ioi", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_messages_v2(get_token["user_2"]["token"], channel_id, 0)


def test_channel_messages_v2_success_more_than_50_messages(get_token):
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", True)["channel_id"]
    for i in range(0, 110):
        message_send_v1(get_token["user_1"]["token"], channel_id, str(i))

    channel = help.searching_channel_with_channel_id(channel_id)
    content_list = []
    for i in range(40, 90):
        content_list.append(channel["message"][i])

    assert channel_messages_v2(get_token["user_1"]["token"], channel_id, 40) == {
        "messages": content_list,
        "start": 40,
        "end": 90
    }
    content_list = []
    for i in range(90, 110):
        content_list.append(channel["message"][i])
    assert channel_messages_v2(get_token["user_1"]["token"], channel_id, 90) == {
        "messages": content_list,
        "start": 90,
        "end": -1
    }
    content_list = []
    for i in range(60, 110):
        content_list.append(channel["message"][i])
    assert channel_messages_v2(get_token["user_1"]["token"], channel_id, 60) == {
        "messages": content_list,
        "start": 60,
        "end": -1
    }


def test_messages_success_send_more_channel(get_token):
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


def test_channel_messages_v2_less_than_50_message(get_token):
    channel_id = channels_create_v2(
        get_token['user_1']["token"], "fxghh_channel", True)["channel_id"]
    for i in range(0, 1):
        message_send_v1(get_token["user_1"]["token"], channel_id, str(i))

    channel = help.searching_channel_with_channel_id(channel_id)
    content_list = []
    for i in range(0, 1):
        content_list.append(channel["message"][i])

    assert channel_messages_v2(get_token["user_1"]["token"], channel_id, 0) == {
        "messages": content_list,
        "start": 0,
        "end": -1
    }
