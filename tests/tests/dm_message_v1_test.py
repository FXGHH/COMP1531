from os import access
import pytest
from src.message import message_senddm_v1
from src.data_store import data_store
from src.dm import dm_create_v1, dm_messages_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
import src.help as help


@pytest.fixture
def init_set():
    clear_v1()
    user_1 = auth_register_v2(
        'abcsadadadaa@qq.com', '123123123123', 'Jake', 'Re')
    user_2 = auth_register_v2(
        'cbajojojpjo@qq.com', '111233333333', 'God', 'jj')
    user_3 = auth_register_v2(
        'cbaggggggggggggg@qq.com', '111233333333', 'pweod', 'qwerdf')
    user_4 = auth_register_v2(
        'cnnsw@qq.com', '1453333', 'Jeff', 'Swift')
    u_id_2 = help.get_auth_user_id(user_2["token"])
    u_id_3 = help.get_auth_user_id(user_3["token"])
    dm_id = dm_create_v1(user_1["token"], [u_id_2, u_id_3])["dm_id"]
    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "user_4": user_4, "dm_id": dm_id}


# invalid Channel ID
def test_dm_messages_v1_no_channel_found(init_set):
    with pytest.raises(InputError):
        dm_messages_v1(init_set["user_1"]["token"], 101, 0)


# invalid token
def test_dm_messages_v1_invild_token(init_set):
    with pytest.raises(AccessError):
        dm_messages_v1('abc', init_set["dm_id"], 0)


# out the range of messages index
def test_dm_messages_v1_out_range_messages(init_set):
    message_senddm_v1(init_set['user_1']["token"], init_set["dm_id"],
                      "We are the best")
    with pytest.raises(InputError):
        dm_messages_v1(init_set["user_1"]
                       ["token"], init_set["dm_id"], 100)


# no message in channel
def test_dm_messages_v1_no_message(init_set):
    assert dm_messages_v1(init_set["user_1"]["token"], init_set["dm_id"], 0) == {
        "messages": [],
        "start": 0,
        "end": -1
    }


# Can't access the channel
def test_dm_messages_v1_invild_access(init_set):
    with pytest.raises(AccessError):
        dm_messages_v1(init_set["user_4"]["token"],
                       init_set["dm_id"], 0)


def test_dm_messages_v1_success_more_than_50_messages(init_set):
    for i in range(0, 110):
        message_senddm_v1(init_set["user_1"]["token"],
                          init_set["dm_id"], str(i))

    dm = help.searching_dm_with_dm_id(init_set["dm_id"])
    content_list = []
    for i in range(40, 90):
        content_list.append(dm["dm_messages"][i])

    assert dm_messages_v1(init_set["user_1"]["token"], init_set["dm_id"], 40) == {
        "messages": content_list,
        "start": 40,
        "end": 90
    }
    content_list = []
    for i in range(90, 110):
        content_list.append(dm["dm_messages"][i])
    assert dm_messages_v1(init_set["user_1"]["token"], init_set["dm_id"], 90) == {
        "messages": content_list,
        "start": 90,
        "end": -1
    }
    content_list = []
    for i in range(60, 110):
        content_list.append(dm["dm_messages"][i])
    assert dm_messages_v1(init_set["user_1"]["token"], init_set["dm_id"], 60) == {
        "messages": content_list,
        "start": 60,
        "end": -1
    }


# def test_messages_success_send_more_channel(init_set):
#     channel_id = channels_create_v2(
#         init_set['user_1']["token"], "fxghh_channel", False)["channel_id"]
#     message_send_v1(init_set['user_1']["token"], channel_id,
#                     "We are the best")
#     message_detail = channel_messages_v2(
#         init_set['user_1']["token"], channel_id, 0)
#     assert message_detail["start"] == 0
#     assert message_detail["end"] == -1
#     assert message_detail["messages"][0]["message_id"] == 1
#     assert message_detail["messages"][0]["u_id"] == 1
#     assert message_detail["messages"][0]["message"] == "We are the best"


def test_dm_messages_v1_less_than_50_message(init_set):
    for i in range(0, 20):
        message_senddm_v1(init_set["user_1"]["token"],
                          init_set["dm_id"], str(i))

    dm = help.searching_dm_with_dm_id(init_set["dm_id"])
    content_list = []
    for i in range(0, 20):
        content_list.append(dm["dm_messages"][i])

    assert dm_messages_v1(init_set["user_1"]["token"], init_set["dm_id"], 0) == {
        "messages": content_list,
        "start": 0,
        "end": -1
    }
