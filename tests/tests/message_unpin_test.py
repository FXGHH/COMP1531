import pytest
from src.data_store import data_store
from src.channel import channel_messages_v2, channel_invite_v2
from src.message import message_send_v1, message_remove_v1, message_senddm_v1, message_share_v1, message_unpin_v1, message_pin_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
import src.help as help


@pytest.fixture
def fix():
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


def test_messages_unpin_invalid_token(fix):
    with pytest.raises(AccessError):
        message_unpin_v1("abc", fix["channel_message_id_1"])


def test_messages_unpin_invalid_message_id(fix):
    with pytest.raises(InputError):
        message_unpin_v1(fix["user_1"]["token"], 101)


def test_messages_unpin_user_unpermission_in_channle_1(fix):
    with pytest.raises(AccessError):
        message_unpin_v1(fix["user_2"]["token"], fix["channel_message_id_1"])


# def test_messages_unpin_user_unpermission_in_channle_2(fix):
#     channel_invite_v2(fix["user_1"]["token"],
#                       fix["channel_message_id_1"], fix["user_4"]['auth_user_id'])
#     with pytest.raises(AccessError):
#         message_unpin_v1(fix["user_4"]["token"], fix["channel_message_id_1"])


def test_messages_unpin_user_unpermission_in_dm_1(fix):
    with pytest.raises(AccessError):
        message_unpin_v1(fix["user_1"]["token"], fix["dm_message_id_1"])


def test_messages_unpin_user_unpermission_in_dm_2(fix):
    with pytest.raises(AccessError):
        message_unpin_v1(fix["user_3"]["token"], fix["dm_message_id_1"])


def test_messages_unpin_success_in_channle(fix):
    message_pin_v1(fix["user_1"]["token"], fix["channel_message_id_1"])
    message_unpin_v1(fix["user_1"]["token"], fix["channel_message_id_1"])
    message_detail = channel_messages_v2(
        fix["user_1"]["token"], fix["channel_id"], 0)
    assert message_detail['messages'][0]["is_pinned"] == False


def test_messages_unpin_success_in_dm(fix):
    message_pin_v1(fix["user_2"]["token"], fix["dm_message_id_1"])
    message_unpin_v1(fix["user_2"]["token"], fix["dm_message_id_1"])
    message_detail = dm_messages_v1(
        fix["user_2"]["token"], fix["dm_id"], 0)
    assert message_detail['messages'][0]["is_pinned"] == False


def test_messages_unpin_already_unpinned_in_channle(fix):
    with pytest.raises(InputError):
        message_unpin_v1(fix["user_1"]["token"], fix["channel_message_id_1"])


def test_messages_unpin_already_unpinned_in_dm(fix):
    with pytest.raises(InputError):
        message_unpin_v1(fix["user_2"]["token"], fix["dm_message_id_1"])
