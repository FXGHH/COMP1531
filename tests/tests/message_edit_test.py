from os import access
import pytest
from src.message import message_send_v1, message_senddm_v1, message_edit_v1
from src.data_store import data_store
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.error import InputError, AccessError
from src.other import clear_v1
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
        'cbaggggggggggggg@qq.com', '121990211', 'pweod', 'qwerdf')
    user_4 = auth_register_v2(
        'cnnsw@qq.com', '1453333', 'Jeff', 'Swift')

    channel_id_1 = channels_create_v2(
        user_1["token"], "fxghh channel", False)["channel_id"]
    channel_id_2 = channels_create_v2(
        user_2["token"], "Eric channel", False)["channel_id"]

    u_id_2 = help.get_auth_user_id(user_2["token"])
    u_id_3 = help.get_auth_user_id(user_3["token"])
    dm_id = dm_create_v1(user_1["token"], [u_id_2, u_id_3])["dm_id"]
    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "user_4": user_4, "dm_id": dm_id,
            "channel_id_1": channel_id_1, "channel_id_2": channel_id_2}


def test_message_edit_v1_invild_message_length(init_set):
    dm_message_id = message_senddm_v1(
        init_set['user_1']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    with pytest.raises(InputError):
        message_edit_v1(init_set['user_1']["token"], dm_message_id, "u"*1001)


def test_message_edit_v1_invalid_token(init_set):
    dm_message_id = message_senddm_v1(
        init_set['user_1']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    with pytest.raises(AccessError):
        message_edit_v1('abc', dm_message_id, "Change message")


def test_message_edit_v1_no_message_id_found(init_set):
    message_send_v1(init_set["user_1"]["token"],
                    init_set["channel_id_1"], "We are the best")
    message_senddm_v1(
        init_set['user_1']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    with pytest.raises(InputError):
        message_edit_v1(init_set["user_1"]["token"],
                        101, "Change message")


def test_message_edit_v1_not_authorised_user_channle(init_set):
    channel_message_id = message_send_v1(init_set["user_1"]["token"],
                                         init_set["channel_id_1"], "We are the best")["message_id"]
    message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "Hi there !")
    with pytest.raises(AccessError):
        message_edit_v1(init_set["user_2"]["token"],
                        channel_message_id, "Change message")


def test_message_edit_v1_not_authorised_user_dm(init_set):
    message_send_v1(init_set["user_1"]["token"],
                    init_set["channel_id_1"], "We are the best")["message_id"]
    dm_message_id = message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    with pytest.raises(AccessError):
        message_edit_v1(init_set["user_3"]["token"],
                        dm_message_id, "Change message")


def test_message_edit_v1_dm_empty_message(init_set):
    message_send_v1(init_set["user_1"]["token"],
                    init_set["channel_id_1"], "We are the best")["message_id"]
    dm_message_id = message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    message_edit_v1(init_set["user_2"]["token"],
                    dm_message_id, "")
    assert help.message_id_is_valid_in_dm(dm_message_id) == False


def test_message_edit_v1_channle_empty_message(init_set):
    channel_message_id = message_send_v1(init_set["user_1"]["token"],
                                         init_set["channel_id_1"], "We are the best")["message_id"]
    message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "Hi there !")
    message_edit_v1(init_set["user_1"]["token"],
                    channel_message_id, "")
    assert help.message_id_is_valid_in_channel(channel_message_id) == False


def test_message_edit_v1_channel_message_success_edit(init_set):
    channel_message_id = message_send_v1(init_set["user_1"]["token"],
                                         init_set["channel_id_1"], "We are the best")["message_id"]
    message_edit_v1(init_set["user_1"]["token"],
                    channel_message_id, "Changed message")
    assert help.find_message_in_channel(channel_message_id)[
        "message"] == "Changed message"


def test_message_edit_v1_channel_message_success_edit_2(init_set):
    message_send_v1(init_set["user_1"]["token"],
                    init_set["channel_id_1"], "aaaaa")["message_id"]
    channel_message_id = message_send_v1(init_set["user_1"]["token"],
                                         init_set["channel_id_1"], "We are the best")["message_id"]
    message_send_v1(init_set["user_1"]["token"],
                    init_set["channel_id_1"], "bbbbb")["message_id"]
    message_send_v1(init_set["user_1"]["token"],
                    init_set["channel_id_1"], "ccccc")

    message_edit_v1(init_set["user_1"]["token"],
                    channel_message_id, "Changed message")
    assert help.find_message_in_channel(channel_message_id)[
        "message"] == "Changed message"


def test_message_edit_v1_dm_message_success_edit(init_set):
    dm_message_id = message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    message_edit_v1(init_set["user_2"]["token"],
                    dm_message_id, "Chnaged message")
    assert help.find_message_in_dm(dm_message_id)[
        "message"] == "Chnaged message"


def test_message_edit_v1_dm_message_success_edit_2(init_set):
    message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "iooioioioi")["message_id"]
    dm_message_id = message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "Hi there !")["message_id"]
    message_senddm_v1(
        init_set['user_2']["token"], init_set["dm_id"], "gg gg gg gg")["message_id"]

    message_edit_v1(init_set["user_2"]["token"],
                    dm_message_id, "Chnaged message")
    assert help.find_message_in_dm(dm_message_id)[
        "message"] == "Chnaged message"
