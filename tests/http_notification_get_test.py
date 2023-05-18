import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
import time
OK_STATUS = 200

def test_token_error():
    requests.delete(config.url + "/clear/v1")
    res = requests.get(config.url + "/notifications/get/v1", params = {'token': "",})
    assert res.status_code == 403

def test_correct_get_notifications():
    requests.delete(config.url + "/clear/v1")
    # register user
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "AA",
        "name_last": "AA"
    }).json()

    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@outlook.com",
        "password": "123456",
        "name_first": "BB",
        "name_last": "BB"
    }).json()

    user3 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcddd@outlook.com",
        "password": "123456",
        "name_first": "CC",
        "name_last": "CC"
    }).json()

    user4 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcddddd@outlook.com",
        "password": "123456",
        "name_first": "DD",
        "name_last": "DD"
    }).json()
    #create channels
    channel1 = requests.post(config.url + "channels/create/v2", json={
        "token": user1["token"],
        "name": "a",
        "is_public": True
    }).json()
    channel2 = requests.post(config.url + "channels/create/v2", json={
        "token": user2["token"],
        "name": "b",
        "is_public": True
    }).json()
    # dm create
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [2]
    }).json()
    # invite
    requests.post(config.url + "channel/invite/v2", json={
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user2["token"]
    })
    requests.post(config.url + "channel/invite/v2", json={
        "token": user2["token"],
        "channel_id": channel2["channel_id"],
        "u_id": user1["token"]
    })

    # ch message send

    requests.post(config.url + "message/send/v1", json={
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "message": "@bbbb"
    })
    requests.post(config.url + "message/send/v1", json={
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "message": "@dddd @eeee"
    })

    requests.post(config.url + "message/send/v1", json={
        "token": user3["token"],
        "channel_id": channel1["channel_id"],
        "message": "@dddd @eeee @aaaa @cccc @bbbb"
    })

    requests.post(config.url + "message/senddm/v1", json={
        "token": user2["token"],
        "dm_id": dm1['dm_id'],
        "message": "@bbbb"
    })
    requests.post(config.url + "message/senddm/v1", json={
        "token": user2["token"],
        "dm_id": dm1['dm_id'],
        "message": "@dddd @eeee"
    })

    requests.post(config.url + "message/senddm/v1", json={
        "token": user4["token"],
        "dm_id": dm1['dm_id'],
        "message": "@dddd @eeee @aaaa @cccc @bbbb"
    })

    #ch sendlater
    current_time_ch1 = int(time.time())
    time_sent_ch1 = current_time_ch1 + 2
    requests.post(config.url + "message/sendlater/v1", json={
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "message": "@bbbb",
        "time_sent": time_sent_ch1 + 50
    })

    current_time_ch2 = int(time.time())
    time_sent_ch2 = current_time_ch2 + 2
    requests.post(config.url + "message/sendlater/v1", json={
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "message": "@dddd @eeee",
        "time_sent": time_sent_ch2 + 50
    })

    current_time_ch3 = int(time.time())
    time_sent_ch3 = current_time_ch3 + 2
    requests.post(config.url + "message/sendlater/v1", json={
        "token": user3["token"],
        "channel_id": channel1["channel_id"],
        "message": "@dddd @eeee @aaaa @cccc @bbbb",
        "time_sent": time_sent_ch3 + 50
    })


    # dm sendlater
    current_time_dm1 = int(time.time())
    time_sent_dm1 = current_time_dm1 + 2
    requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": user2["token"],
        "dm_id": dm1['dm_id'],
        "message": "@bbbb",
        "time_sent": time_sent_dm1 + 50
    })

    current_time_dm2 = int(time.time())
    time_sent_dm2 = current_time_dm2 + 2
    requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": user2["token"],
        "dm_id": dm1['dm_id'],
        "message": "@dddd @eeee",
        "time_sent": time_sent_dm2 + 50
    }).status_code

    current_time_dm3 = int(time.time())
    time_sent_dm3 = current_time_dm3 + 2
    requests.post(config.url + "message/sendlaterdm/v1", json={
        "token": user3["token"],
        "dm_id": dm1['dm_id'],
        "message": "@dddd @eeee @aaaa @cccc @bbbb",
        "time_sent": time_sent_dm3 + 50
    })


    # share
    requests.post(config.url + "message/share/v1", json={
        "token": user2["token"],
        "og_message_id": 1,
        "message": "@bbbb",
        "channel_id": channel2["channel_id"],
        "dm_id": -1,
    })

    requests.post(config.url + "message/share/v1", json={
        "token": user2["token"],
        "og_message_id": 1,
        "message": "@dddd @eeee",
        "channel_id": channel2["channel_id"],
        "dm_id": -1,
    })

    requests.post(config.url + "message/share/v1", json={
        "token": user2["token"],
        "og_message_id": 1,
        "message": "@bbbb",
        "channel_id": -1,
        "dm_id": dm1['dm_id'],
    })

    requests.post(config.url + "message/share/v1", json={
        "token": user2["token"],
        "og_message_id": 1,
        "message": "@dddd @eeee",
        "channel_id": -1,
        "dm_id": dm1['dm_id'],
    })

    # edit
    requests.put(config.url + "message/edit/v1", json={
        "token": user2["token"],
        "message_id": 1,
        "message": '@bbbb'
    })

    requests.put(config.url + "message/edit/v1", json={
        "token": user2["token"],
        "message_id": 1,
        "message": '@dddd @eeee'
    })

    requests.put(config.url + "message/edit/v1", json={
        "token": user2["token"],
        "message_id": 2,
        "message": '@bbbb'
    })

    requests.put(config.url + "message/edit/v1", json={
        "token": user2["token"],
        "message_id": 2,
        "message": '@dddd @eeee'
    })



    # react
    requests.post(config.url + "message/react/v1", json={
        "token": user2["token"],
        "message_id": 1,
        "react_id": 1,
    })

    requests.post(config.url + "message/react/v1", json={
        "token": user2["token"],
        "message_id": 2,
        "react_id": 1,
    })

    requests.post(config.url + "message/react/v1", json={
        "token": user3["token"],
        "message_id": 2,
        "react_id": 1,
    })

    requests.post(config.url + "message/react/v1", json={
        "token": user4["token"],
        "message_id": 2,
        "react_id": 1,
    })

    requests.post(config.url + "message/react/v1", json={
        "token": user4["token"],
        "message_id": 1,
        "react_id": 1,
    })

    requests.post(config.url + "message/react/v1", json={
        "token": user3["token"],
        "message_id": 1,
        "react_id": 1,
    })






    #test

    assert requests.get(config.url + "notifications/get/v1", params = {
        "token": user2["token"],
    }).status_code == OK_STATUS

    assert requests.get(config.url + "notifications/get/v1", params = {
        "token": user1["token"],
    }).status_code == OK_STATUS

    assert requests.get(config.url + "notifications/get/v1", params = {
        "token": user3["token"],
    }).status_code == OK_STATUS

    
    assert requests.get(config.url + "notifications/get/v1", params = {
        "token": user4["token"],
    }).status_code == OK_STATUS

    
