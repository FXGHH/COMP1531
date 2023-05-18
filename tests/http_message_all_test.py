import json
from urllib import response
import pytest
import requests
from src import config
import time
OK_STATUS = 200


@pytest.fixture
def mess_init():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": 'abcsadadadaa@qq.com',
        "password": '123123123123',
        "name_first": 'Jake',
        "name_last": 'Re'
    }).json()
    user_2 = requests.post(config.url + "auth/register/v2", json={
        "email": 'cbajojojpjo@qq.com',
        "password": '111233333333Abc',
        "name_first": 'God',
        "name_last": 'Belo'
    }).json()
    user_3 = requests.post(config.url + "auth/register/v2", json={
        "email": 'cbaggggggggggggg@gmail.com',
        "password": '789shkiiII',
        "name_first": 'yiyo',
        "name_last": 'qwerdf'
    }).json()
    user_4 = requests.post(config.url + "auth/register/v2", json={
        "email": 'twbbcd@gmail.com',
        "password": '32321ssk',
        "name_first": 'yomi',
        "name_last": 'king'
    }).json()
    channel_1 = requests.post(config.url + "channels/create/v2", json={
        "token": user_1["token"],
        "name": "fxghh channel",
        "is_public": True
    }).json()
    message_id = requests.post(config.url + "message/send/v1", json={
        "token": user_1["token"],
        "channel_id": channel_1["channel_id"],
        "message": "We are the best"
    }).json()
    dm_id_1 = requests.post(config.url + "dm/create/v1", json={
        "token": user_1["token"],
        "u_ids": [user_2["auth_user_id"], user_3["auth_user_id"]]
    }).json()
    dm_message_id_1 = requests.post(config.url + "message/senddm/v1", json={
        "token": user_1["token"],
        "dm_id": dm_id_1["dm_id"],
        "message": "Hello World"
    }).json()
    dm_message_id_2 = requests.post(config.url + "message/senddm/v1", json={
        "token": user_2["token"],
        "dm_id": dm_id_1["dm_id"],
        "message": "Hi there!!"
    }).json()

    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "user_4": user_4, "channel_1": channel_1,
            "message_id": message_id, "dm_id_1": dm_id_1, "dm_message_id_1": dm_message_id_1, "dm_message_id_2": dm_message_id_2}


########################## channel meesage send test ###########################
def test_message_send_input_large_1000(mess_init):
    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "a"*1001
    }).status_code == 400


def test_message_send_invalid_access(mess_init):
    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_2"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "We are the best"
    }).status_code == 403


def test_message_send_input_less_1(mess_init):
    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": ""
    }).status_code == 400


def test_message_send_invalid_token(mess_init):
    assert requests.post(config.url + "message/send/v1", json={
        "token": "abc",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "We are the best"
    }).status_code == 403


def test_message_send_invalid_channel_id(mess_init):
    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": 9999,
        "message": "We are the best"
    }).status_code == 400


def test_message_send_success(mess_init):
    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "We are the best"
    }).status_code == 200


def test_message_send_success_more_channel(mess_init):
    channel_2 = requests.post(config.url + "channels/create/v2", json={
        "token": mess_init["user_1"]["token"],
        "name": "fxghh_2 channel",
        "is_public": True
    }).json()

    requests.post(config.url + "channel/invite/v2", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": channel_2["channel_id"],
        "u_id": mess_init["user_2"]["auth_user_id"]
    })

    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_2"]["token"],
        "channel_id": channel_2["channel_id"],
        "message": "name is py"
    }).status_code == 200

    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "We are the best"
    }).status_code == 200

######################### channel message remove test ########################


def test_message_remove_invalid_token(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": "abc",
        "message_id": mess_init["message_id"]["message_id"]
    }).status_code == 403


def test_message_remove_invalid_channel_id(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": 11
    }).status_code == 400


def test_channel_message_remove_unpermission_user(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["message_id"]["message_id"]
    }).status_code == 403


def test_message_remove_success_in_channel(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"]
    }).status_code == 200


def test_channel_dm_remove_unpermission_user(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_3"]["token"],
        "message_id": mess_init["dm_message_id_2"]["message_id"]
    }).status_code == 403
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_4"]["token"],
        "message_id": mess_init["dm_message_id_2"]["message_id"]
    }).status_code == 403


def test_dm_message_remove_success(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["dm_message_id_2"]["message_id"]
    }).status_code == 200

    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"]
    }).status_code == 200


def test_dm_message_remove_by_creator_success(mess_init):
    assert requests.delete(config.url + "message/remove/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_2"]["message_id"]
    }).status_code == 200


############################## dm message send test #############################
def test_dm_send_input_large_1000(mess_init):
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "a"*1001
    }).status_code == 400


def test_dm_send_input_less_1(mess_init):
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": ""
    }).status_code == 400


def test_dm_send_invalid_token(mess_init):
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": "invalid token",
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "abc"
    }).status_code == 403


def test_dm_send_invalid_dm_id(mess_init):
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": 12,
        "message": "abc"
    }).status_code == 400


def test_dm_send_not_dm_member(mess_init):
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_4"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "abc"
    }).status_code == 403


def test_dm_send_success(mess_init):
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "abc"
    }).status_code == 200


def test_dm_send_success_more_dm(mess_init):
    dm_id_2 = requests.post(config.url + "dm/create/v1", json={
        "token": mess_init["user_2"]["token"],
        "u_ids": []
    }).json()
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": dm_id_2['dm_id'],
        "message": "Sydney"
    }).status_code == 200
########################### dm message send ###########################


############################# dm message test #############################
def test_dm_messages_inavlid_token(mess_init):
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": "abc",
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 0
    }).status_code == 403


def test_dm_messages_inavlid_dm_id(mess_init):
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": 121,
        "start": 0
    }).status_code == 400


def test_dm_messages_inavlid_member(mess_init):
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_4"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 0
    }).status_code == 403


def test_dm_messages_inavlid_start_index(mess_init):
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 11
    }).status_code == 400


def test_dm_messages_start_index_less_0(mess_init):
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": -1
    }).status_code == 400


def test_dm_messages_start_equal_message_length(mess_init):
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 0
    }).status_code == 200


def test_dm_messages_success_return(mess_init):
    requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "HI all!"
    })
    requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "ABCD"
    })
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 4
    }).status_code == 200


def test_dm_messages_v1_success_respond_more_message(mess_init):
    for i in range(0, 30):
        requests.post(config.url + "message/senddm/v1", json={
            "token": mess_init["user_2"]["token"],
            "dm_id": mess_init["dm_id_1"]['dm_id'],
            "message": str(i)
        })
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["channel_1"]["channel_id"],
        "start": 0
    }).status_code == 200

    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 33
    }).status_code == 400

    for i in range(30, 60):
        requests.post(config.url + "message/senddm/v1", json={
            "token": mess_init["user_1"]["token"],
            "dm_id": mess_init["dm_id_1"]['dm_id'],
            "message": str(i)
        })
    assert requests.get(config.url + "dm/messages/v1", params={
        "token": mess_init["user_1"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "start": 1
    }).status_code == 200
############################# dm message ############################


############################# message edit ############################
def test_message_edit_invalid_token(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": 'abc',
        "message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": 'Changed message'
    }).status_code == 403


def test_message_edit_invalid_message_length(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": 'a'*1001
    }).status_code == 400


def test_message_edit_invalid_message_id(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": 12,
        "message": 'Changed message'
    }).status_code == 400


def test_message_edit_channel_invalid_access_message(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "message": 'Changed message'
    }).status_code == 403


def test_message_edit_dm_invalid_access_message(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_4"]["token"],
        "message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": 'Changed message'
    }).status_code == 403


def test_message_edit_dm_success_edit(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_2"]['message_id'],
        "message": 'Changed message'
    }).status_code == 200

    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["dm_message_id_2"]['message_id'],
        "message": 'Changed message'
    }).status_code == 200

    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_3"]["token"],
        "message_id": mess_init["dm_message_id_2"]['message_id'],
        "message": 'Changed message'
    }).status_code == 403


def test_message_edit_channel_success_edit(mess_init):
    requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "We are the best"
    })
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "message": 'Changed message'
    }).status_code == 200


def test_dm_message_edit_channel_success_edit_remove(mess_init):
    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "message": ''
    }).status_code == 200


def test_message_edit_dm_success_edit_more_message(mess_init):
    # send message to second dm
    dm_id_2 = requests.post(config.url + "dm/create/v1", json={
        "token": mess_init["user_1"]["token"],
        "u_ids": []
    }).json()
    track_message = requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": dm_id_2['dm_id'],
        "message": "abc"
    }).json()
    requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_1"]["token"],
        "dm_id": dm_id_2['dm_id'],
        "message": "KFC better"
    }).json()

    # send message to first dm
    requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
        "message": "abc"
    }).json()

    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": track_message["message_id"],
        "message": 'Changed message'
    }).status_code == 200

    assert requests.put(config.url + "message/edit/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_2"]["message_id"],
        "message": 'Changed message'
    }).status_code == 200
############################# message edit ############################


############################# message share ############################
def test_message_share_invalid_token(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": 'abc',
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 403


def test_message_share_invalid_input_chnanel_dm_id_1(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": -1,
        "dm_id": -1,
    }).status_code == 400


def test_message_share_invalid_input_chnanel_dm_id_2(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": mess_init["dm_id_1"]['dm_id'],
    }).status_code == 400


def test_message_share_invalid_message_id(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": 100,
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 400


def test_message_share_invalid_message_length(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "a"*1001,
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 400


def test_message_share_unauthorized_message_in_channel(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_2"]["token"],
        "og_message_id": mess_init["message_id"]['message_id'],
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 400


def test_message_share_unauthorized_message_in_dm(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_4"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 400


def test_message_share_unauthorized_share_channel(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_2"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 403


def test_message_share_unauthorized_share_dm(mess_init):
    dm_id_2 = requests.post(config.url + "dm/create/v1", json={
        "token": mess_init["user_4"]["token"],
        "u_ids": []
    }).json()
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["message_id"]['message_id'],
        "message": "share a message",
        "channel_id": -1,
        "dm_id": dm_id_2['dm_id'],
    }).status_code == 403


def test_message_share_success_channel_to_channel(mess_init):
    channel_2 = requests.post(config.url + "channels/create/v2", json={
        "token": mess_init["user_1"]["token"],
        "name": "fxghh_2 channel",
        "is_public": True
    }).json()
    requests.post(config.url + "channel/invite/v2", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": channel_2["channel_id"],
        "u_id": mess_init["user_2"]["auth_user_id"]
    })
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["message_id"]['message_id'],
        "message": "share a message",
        "channel_id": channel_2["channel_id"],
        "dm_id": -1,
    }).status_code == 200


def test_message_share_success_channel_to_dm(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["message_id"]['message_id'],
        "message": "share a message",
        "channel_id": -1,
        "dm_id": mess_init["dm_id_1"]['dm_id'],
    }).status_code == 200


def test_message_share_success_dm_to_dm(mess_init):
    dm_id_2 = requests.post(config.url + "dm/create/v1", json={
        "token": mess_init["user_2"]["token"],
        "u_ids": []
    }).json()
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_2"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": -1,
        "dm_id": dm_id_2['dm_id'],
    }).status_code == 200


def test_message_share_success_dm_to_channel(mess_init):
    assert requests.post(config.url + "message/share/v1", json={
        "token": mess_init["user_1"]["token"],
        "og_message_id": mess_init["dm_message_id_1"]['message_id'],
        "message": "share a message",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "dm_id": -1,
    }).status_code == 200
############################## message share ###############################


# ############################## message pin ################################
def test_message_pin_invalid_token(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": "abc",
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 403


def test_message_pin_invalid_message_id(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": 101,
    }).status_code == 400


def test_message_pin_user_unpermission_in_channle_1(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 403


def test_message_pin_user_unpermission_in_channle_2(mess_init):
    requests.post(config.url + "channel/invite/v2", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "u_id": mess_init["user_4"]["auth_user_id"]
    })
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_4"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 403


def test_message_pin_user_unpermission_in_dm_1(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_4"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 403


def test_message_pin_user_unpermission_in_dm_2(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 403


def test_message_pin_success_in_channle(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 200


def test_message_pin_success_in_dm(mess_init):
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 200


def test_message_pin_already_pinned_in_channle(mess_init):
    requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    })
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 400


def test_message_pin_already_pinned_in_dm(mess_init):
    requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    })
    assert requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 400
############################## message pin ################################


############################## message unpin ################################
def test_message_unpin_invalid_token(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": "abc",
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 403


def test_message_unpin_invalid_message_id(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": 101,
    }).status_code == 400


def test_message_unpin_user_unpermission_in_channle_1(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 403


def test_message_unpin_user_unpermission_in_channle_2(mess_init):
    requests.post(config.url + "channel/invite/v2", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "u_id": mess_init["user_4"]["auth_user_id"]
    })
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_4"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 403


def test_message_unpin_user_unpermission_in_dm_1(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_4"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 403


def test_message_unpin_user_unpermission_in_dm_2(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_2"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 403


def test_message_unpin_success_in_channle(mess_init):
    requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    })
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 200


def test_message_unpin_success_in_dm(mess_init):
    requests.post(config.url + "message/pin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    })
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 200


def test_message_pin_already_unpin_in_channle(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
    }).status_code == 400


def test_message_pin_already_unpin_in_dm(mess_init):
    assert requests.post(config.url + "message/unpin/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
    }).status_code == 400
############################## message unpin ################################


############################## message react ################################
def test_message_react_invalid_token(mess_init):
    assert requests.post(config.url + "message/react/v1", json={
        "token": "abc",
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    }).status_code == 403


def test_message_react_invalid_message_id(mess_init):
    assert requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": -1,
        "react_id": 1,
    }).status_code == 400


def test_message_react_invalid_react_id(mess_init):
    assert requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 3,
    }).status_code == 400


def test_message_react_success_react_and_already_reacted(mess_init):
    assert requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    }).status_code == 200
    assert requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    }).status_code == 400

    assert requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
        "react_id": 1,
    }).status_code == 200
    assert requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
        "react_id": 1,
    }).status_code == 400
############################## message react ################################


############################## message unreact ##############################
def test_message_unreact_invalid_token(mess_init):
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": "abc",
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    }).status_code == 403


def test_message_unreact_invalid_message_id(mess_init):
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": -1,
        "react_id": 1,
    }).status_code == 400


def test_message_unreact_invalid_react_id(mess_init):
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 3,
    }).status_code == 400


def test_message_unreact_success_react_and_already_unreact(mess_init):
    requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    })
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    }).status_code == 200
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["message_id"]["message_id"],
        "react_id": 1,
    }).status_code == 400

    requests.post(config.url + "message/react/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
        "react_id": 1,
    }).status_code == 200
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
        "react_id": 1,
    }).status_code == 200
    assert requests.post(config.url + "message/unreact/v1", json={
        "token": mess_init["user_1"]["token"],
        "message_id": mess_init["dm_message_id_1"]["message_id"],
        "react_id": 1,
    }).status_code == 400
############################## message unreact ##############################


########################## channel message sendlater ########################
def test_message_sendlater_invalid_token(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": "abc",
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 403


def test_message_sendlater_invalid_message_length(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": 'a'*1001,
        "time_sent": time_sent
    }).status_code == 400
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": '',
        "time_sent": time_sent
    }).status_code == 400


def test_message_sendlater_invalid_channel_id(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": -1,
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 400


def test_message_sendlater_invalid_time_send(mess_init):
    current_time = int(time.time())
    time_sent = current_time - 1
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 400


def test_message_sendlater_not_member(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_2"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 403


def test_message_sendlater_success(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    # add an irrelevant later channel_message
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "irrelevant messaeg",
        "time_sent": time_sent + 50
    }).status_code == 200
    assert requests.post(config.url + "message/sendlater/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 200
    time.sleep(2)
    # run the inside channel message send through check the send_later_message dic
    assert requests.post(config.url + "message/send/v1", json={
        "token": mess_init["user_1"]["token"],
        "channel_id": mess_init["channel_1"]["channel_id"],
        "message": "future messaeg",
    }).status_code == 200
########################## channel message sendlater ########################


############################## dm message sendlater ##########################
def test_message_sendlaterdm_invalid_token(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": "abc",
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 403


def test_message_sendlaterdm_invalid_message_length(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": 'a'*1001,
        "time_sent": time_sent
    }).status_code == 400
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": '',
        "time_sent": time_sent
    }).status_code == 400


def test_message_sendlaterdm_invalid_channel_id(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": -1,
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 400


def test_message_sendlaterdm_invalid_time_send(mess_init):
    current_time = int(time.time())
    time_sent = current_time - 1
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 400


def test_message_sendlaterdm_not_member(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_4"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 403


def test_message_sendlaterdm_success(mess_init):
    current_time = int(time.time())
    time_sent = current_time + 2
    # add an irrelevant later dm_message
    requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": "irrelevant messaeg",
        "time_sent": time_sent + 50
    }).status_code == 200
    assert requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": "future messaeg",
        "time_sent": time_sent
    }).status_code == 200
    time.sleep(2)
    # run the inside message_senddm through check the send_later_dmmessage dic
    assert requests.post(config.url + "message/senddm/v1", json={
        "token": mess_init["user_2"]["token"],
        "dm_id": mess_init["dm_id_1"]["dm_id"],
        "message": "future messaeg",
    }).status_code == 200
############################## dm message sendlater ##########################
