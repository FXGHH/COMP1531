import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
# test in differnt situation
def test_channel_join_public_privare_no_chid_self_ch():

    requests.delete(config.url + "/clear/v1")

    user_1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    user_2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@gmail.com",
        "password": "12345678",
        "name_first": "Jake1",
        "name_last": "Renzella2"
    }).json()
    user_3 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcde@gmail.com",
        "password": "123456789",
        "name_first": "Jake11",
        "name_last": "Renzella22"
    }).json()

    channel_1 = requests.post(config.url + "channels/create/v2", json = {
        "token": user_1["token"],
        "name": "channel_1",
        "is_public": False
    }).json()
    channel_2 = requests.post(config.url + "channels/create/v2", json = {
        "token": user_2["token"],
        "name": "channel_2",
        "is_public": True
    }).json()
    channel_3 = requests.post(config.url + "channels/create/v2", json = {
        "token": user_3["token"],
        "name": "channel_3",
        "is_public": False
    }).json()

    # join public
    join_1 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_2["channel_id"]
    })

    join_2 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_3["token"],
        "channel_id": channel_2["channel_id"]
    })

    join_3 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_1["channel_id"]
    })

    join_4 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_3["channel_id"]
    })
    assert join_1.status_code == OK_STATUS
    assert join_2.status_code == OK_STATUS
    assert join_3.status_code == 400
    assert join_4.status_code == OK_STATUS

    # join private
    join_5 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_3["channel_id"]
    })
    join_6 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_2["token"],
        "channel_id": channel_3["channel_id"]
    })
    assert join_5.status_code == 400
    assert join_6.status_code == 403

    # already in
    join_7 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_1["channel_id"]
    })
    join_8 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_2["token"],
        "channel_id": channel_2["channel_id"]
    })
    join_9 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_3["token"],
        "channel_id": channel_3["channel_id"]
    })
    assert join_7.status_code == 400
    assert join_8.status_code == 400
    assert join_9.status_code == 400

    # no ch id
    join_10 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": 4
    })
    join_11 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": 5
    })
    join_12 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": 6
    })
    assert join_10.status_code == 400
    assert join_11.status_code == 400
    assert join_12.status_code == 400

def test_global_join():
    requests.delete(config.url + "/clear/v1")

    user_1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    user_2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@gmail.com",
        "password": "12345678",
        "name_first": "Jake1",
        "name_last": "Renzella2"
    }).json()
    user_3 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcde@gmail.com",
        "password": "123456789",
        "name_first": "Jake11",
        "name_last": "Renzella22"
    }).json()

    channel_1 = requests.post(config.url + "channels/create/v2", json = {
        "token": user_1["token"],
        "name": "channel_1",
        "is_public": False
    }).json()
    channel_2 = requests.post(config.url + "channels/create/v2", json = {
        "token": user_2["token"],
        "name": "channel_2",
        "is_public": True
    }).json()
    channel_3 = requests.post(config.url + "channels/create/v2", json = {
        "token": user_3["token"],
        "name": "channel_3",
        "is_public": False
    }).json()

    # global_onwer_join
    join_13 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_1["channel_id"]
    })
    join_14 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_2["channel_id"]
    })
    join_15 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": channel_3["channel_id"]
    })
    join_16 = requests.post(config.url + "channel/join/v2", json = {
        "token": user_1["token"],
        "channel_id": 4
    })
    assert join_13.status_code == 400
    assert join_14.status_code == OK_STATUS
    assert join_15.status_code == OK_STATUS
    assert join_16.status_code == 400

# join with incorrect token
def test_token_error():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
        
    channel_1 = requests.post(config.url + "channels/create/v2", json = {
        "token": user["token"],
        "name": "channel_1",
        "is_public": False
    }).json()
    join_1 = requests.post(config.url + "channel/join/v2", json = {
        "token": '',
        "channel_id": channel_1["channel_id"]
    })
    assert join_1.status_code == 403
# join with member already in channel
def test_is_member():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcdas@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    channel_1 = requests.post(config.url + "channels/create/v2", json = {
        "token": user1["token"],
        "name": "channel_1",
        "is_public": False
    }).json()

    join_1 = requests.post(config.url + "channel/join/v2", json = {
        "token": user2["token"],
        "channel_id": channel_1["channel_id"]
    })
    assert join_1.status_code == 403