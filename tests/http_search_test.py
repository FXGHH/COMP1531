import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200

def test_token_error():
    requests.delete(config.url + "/clear/v1")
    res = requests.get(config.url + 'search/v1', params = {'token': "", 'query_str': "as"})
    assert res.status_code == 403

def test_query_less_than_1():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    res = requests.get(config.url + 'search/v1', params = {'token': user1["token"], 'query_str': ""})
    assert res.status_code == 400

def test_query_more_than_1000():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    res = requests.get(config.url + 'search/v1', params = {'token': user1["token"], 'query_str': "1" * 1111})
    assert res.status_code == 400

def test_correct_search_message():
    requests.delete(config.url + "/clear/v1")
    # register user
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
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
    # join channels
    requests.post(config.url + "channel/join/v2", json = {
        "token": user1["token"],
        "channel_id": channel2["channel_id"]
    })

    requests.post(config.url + "channel/join/v2", json = {
        "token": user2["token"],
        "channel_id": channel1["channel_id"]
    })
    # dm create
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [2]
    }).json()

    dm2 = requests.post(config.url + "dm/create/v1", json = {
        "token": user2["token"],
        "u_ids": [1]
    }).json()

    # ch message send
    requests.post(config.url + "message/send/v1", json={
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "message": "1a"
    })
    requests.post(config.url + "message/send/v1", json={
        "token": user1["token"],
        "channel_id": channel2["channel_id"],
        "message": "2a"
    })

    requests.post(config.url + "message/send/v1", json={
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "message": "1b"
    })
    requests.post(config.url + "message/send/v1", json={
        "token": user2["token"],
        "channel_id": channel2["channel_id"],
        "message": "2b"
    })

    # dm message send
    requests.post(config.url + "message/senddm/v1", json={
        "token": user1["token"],
        "dm_id": dm1['dm_id'],
        "message": "1a"
    })
    requests.post(config.url + "message/senddm/v1", json={
        "token": user1["token"],
        "dm_id": dm2['dm_id'],
        "message": "2a"
    })
    requests.post(config.url + "message/senddm/v1", json={
        "token": user2["token"],
        "dm_id": dm1['dm_id'],
        "message": "1b"
    })
    requests.post(config.url + "message/senddm/v1", json={
        "token": user2["token"],
        "dm_id": dm2['dm_id'],
        "message": "2b"
    })
    # search
    resp1 = requests.get(config.url + "search/v1", params = {
        "token": user1["token"],
        "query_str": "1"
    })
    assert resp1.status_code == OK_STATUS

    resp2 = requests.get(config.url + "search/v1", params = {
        "token": user1["token"],
        "query_str": "2"
    })
    assert resp2.status_code == OK_STATUS

    resp3 = requests.get(config.url + "search/v1", params = {
        "token": user2["token"],
        "query_str": "1"
    })
    assert resp3.status_code == OK_STATUS

    resp4 = requests.get(config.url + "search/v1", params = {
        "token": user2["token"],
        "query_str": "2"
    })
    assert resp4.status_code == OK_STATUS
