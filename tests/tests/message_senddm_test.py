from os import access
import pytest
from src.message import message_send_v1, message_senddm_v1
from src.data_store import data_store
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
        'cbaggggggggggggg@qq.com', '111233333333', 'pweod', 'qwerdf')
    user_4 = auth_register_v2(
        'cnnsw@qq.com', '1453333', 'Jeff', 'Swift')
    u_id_2 = help.get_auth_user_id(user_2["token"])
    u_id_3 = help.get_auth_user_id(user_3["token"])
    dm_id = dm_create_v1(user_1["token"], [u_id_2, u_id_3])["dm_id"]
    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "user_4": user_4, "dm_id": dm_id}


def test_dm_senddm_v1_no_channel_found(init_set):
    with pytest.raises(InputError):
        message_senddm_v1(init_set["user_1"]["token"],
                          101, "this is sunny day")


def test_dm_senddm_v1_invild_token(init_set):
    with pytest.raises(AccessError):
        message_senddm_v1('abc', init_set["dm_id"], "Hi there !")


def test_dm_senddm_v1_not_member(init_set):
    with pytest.raises(AccessError):
        message_senddm_v1(init_set['user_4']["token"], init_set["dm_id"],
                          "We are the best")


def test_dm_senddm_v1_message_less_1(init_set):
    with pytest.raises(InputError):
        message_senddm_v1(init_set['user_1']["token"], init_set["dm_id"],
                          "")


def test_dm_senddm_v1_message_more_1000(init_set):
    string = 'a'
    with pytest.raises(InputError):
        message_senddm_v1(init_set['user_1']["token"], init_set["dm_id"],
                          string*1001)


def test_dm_senddm_v1_message_success(init_set):
    message_senddm_v1(init_set['user_1']["token"],
                      init_set["dm_id"], "Good game")
    dm_dic = help.searching_dm_with_dm_id(init_set["dm_id"])
    assert dm_messages_v1(init_set['user_1']["token"], init_set["dm_id"], 0)[
        "messages"][0] == dm_dic['dm_messages'][0]
