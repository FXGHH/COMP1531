import pytest
import requests
from src import config
from src.server import *
import src.help as help
OK_STATUS = 200


@pytest.fixture
def regis_member():
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
    channel_1 = requests.post(config.url + "channels/create/v2", json={
        "token": user_1["token"],
        "name": "Channel_1",
        "is_public": True
    }).json()
    channel_2 = requests.post(config.url + "channels/create/v2", json={
        "token": user_1["token"],
        "name": "Channel_2",
        "is_public": True
    }).json()
    message_id = requests.post(config.url + "message/send/v1", json={
        "token": user_1["token"],
        "channel_id": channel_1["channel_id"],
        "message": "We are the best"
    }).json()

    return {"user_1": user_1, "user_2": user_2, "user_3": user_3, "channel_1": channel_1, "channel_2": channel_2, "message_id": message_id}


def test_channel_messages_basic_error(regis_member):
    # invlid channel ID
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": 323,
        "start": 0
    }).status_code == 400
    # can't access the channel
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_2"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 10
    }).status_code == 403
    # token is invalid
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": 'abc',
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 0
    }).status_code == 403
    # out range the messages index
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 1000000
    }).status_code == 400


def test_message_v2_message_start_index_less_0(regis_member):
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": -1
    }).status_code == 400


def test_message_v2_success_respond(regis_member):
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 0
    }).status_code == 200

    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_2"]["channel_id"],
        "start": 0
    }).status_code == 200


def test_message_v2_success_respond_more_message(regis_member):
    for i in range(0, 30):
        requests.post(config.url + "message/send/v1", json={
            "token": regis_member["user_1"]["token"],
            "channel_id": regis_member["channel_1"]["channel_id"],
            "message": str(i)
        })
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 0
    }).status_code == 200

    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 33
    }).status_code == 400

    for i in range(30, 60):
        requests.post(config.url + "message/send/v1", json={
            "token": regis_member["user_1"]["token"],
            "channel_id": regis_member["channel_1"]["channel_id"],
            "message": str(i)
        })
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 1
    }).status_code == 200


def test_message_v2_success_respond_len_over_50(regis_member):
    for i in range(0, 70):
        requests.post(config.url + "message/send/v1", json={
            "token": regis_member["user_1"]["token"],
            "channel_id": regis_member["channel_1"]["channel_id"],
            "message": str(i)
        })
    assert requests.get(config.url + "channel/messages/v2", params={
        "token": regis_member["user_1"]["token"],
        "channel_id": regis_member["channel_1"]["channel_id"],
        "start": 0
    }).status_code == 200
