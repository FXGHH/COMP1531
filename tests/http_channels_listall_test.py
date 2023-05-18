import pytest
import requests
from src import config
from src.server import *
OK_STATUS = 200


@pytest.fixture
def users():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "abckdaisdai",
        "name_first": "Eric",
        "name_last": "TSM"
    }).json()
    user_2 = requests.post(config.url + "auth/register/v2", json={
        "email": "aaaa@gmail.com",
        "password": "sswdadadaad",
        "name_first": "smith",
        "name_last": "Jack"
    }).json()
    return {"user_1": user_1, "user_2": user_2}


def test_channels_listall_access_error():
    request = requests.get(config.url + "channels/listall/v2", params={
        "token": 3
    })
    assert request.status_code == 403


def test_channels_listall_success_access(users):
    requests.post(config.url + "channels/create/v2", json={
        "token": users["user_2"]["token"],
        "name": "channel2",
        "is_public": True
    })
    request = requests.get(config.url + "channels/listall/v2", params={
        "token": users["user_1"]["token"]
    })

    assert request.status_code == OK_STATUS


def test_channels_listall_success_access_2(users):
    requests.post(config.url + "channels/create/v2", json={
        "token": users["user_2"]["token"],
        "name": "channel2",
        "is_public": True
    })
    request = requests.get(config.url + "channels/listall/v2", params={
        "token": users["user_2"]["token"]
    })
    assert request.status_code == OK_STATUS
