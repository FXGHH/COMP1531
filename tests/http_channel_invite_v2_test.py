from urllib import response
from src.data_store import data_store
from src.error import AccessError
from src.other import clear_v1
import requests
import pytest
import src.help as help
from src.server import clear_v1
from src import config

INVALID_TOKEN = 'thisisainvalidtoken'
INVALID_CHANNEL_ID = 20
INVALID_U_ID = 50


@pytest.fixture
# this is the fixture that regesiter 3 uers
def users():
    requests.delete(config.url + "clear/v1")
    user1json = requests.post(config.url + "auth/register/v2", json={
        "email": "example@ad.unsw.edu.au.com",
        "password": "passworduser1",
        "name_first": "useronefirst",
        "name_last": "useronelast"
    }).json()
    user2json = requests.post(config.url + "auth/register/v2", json={
        "email": "example2@ad.unsw.edu.au.com",
        "password": "passworduser2",
        "name_first": "usertwofirst",
        "name_last": "usertwolast"
    }).json()
    user3json = requests.post(config.url + "auth/register/v2", json={
        "email": "example3@ad.unsw.edu.au.com",
        "password": "passworduser3",
        "name_first": "userthreefirst",
        "name_last": "userthreelast"
    }).json()
    return {"user1json": user1json,
            "user2json": user2json,
            "user3json": user3json}


@pytest.fixture
# this is the fixture creating new channel with user1's token
def channel(users):
    channel1json = requests.post(config.url + "channels/create/v2", json={
        "token": users["user1json"]["token"],
        "name": "channel1",
        "is_public": True
    }).json()
    return channel1json

#### ### ### ### ###   CHANNEL INVITE   ### ### ### ### ### ### ### ####


def test_invalid_token(channel, users):
    # this test should raises AccessError
    response = requests.post(config.url + "channel/invite/v2", json={
        "token": INVALID_TOKEN,
        "channel_id": channel["channel_id"],
        "u_id": users["user2json"]["auth_user_id"]
    })
    assert response.status_code == 403


def test_invalid_channel_id(users):
    # this test should raises InputError
    response = requests.post(config.url + "channel/invite/v2", json={
        "token": users["user1json"]["token"],
        "channel_id": INVALID_CHANNEL_ID,
        "u_id": users["user2json"]["auth_user_id"]
    })
    assert response.status_code == 400


def test_invalid_u_id(users, channel):
    # this test should raises InputError
    response = requests.post(config.url + "channel/invite/v2", json={
        "token": users["user1json"]["token"],
        "channel_id": channel["channel_id"],
        "u_id": INVALID_U_ID
    })
    assert response.status_code == 400


def test_invalid_reinvite(users, channel):
    # this tests should raises InputError
    response = requests.post(config.url + "channel/invite/v2", json={
        "token": users["user1json"]["token"],
        "channel_id": channel["channel_id"],
        "u_id": users["user1json"]["auth_user_id"]
    })
    assert response.status_code == 400


def test_not_auth_user(users, channel):
    # this test should raises AccessError
    response = requests.post(config.url + "channel/invite/v2", json={
        "token": users["user2json"]["token"],
        "channel_id": channel["channel_id"],
        "u_id": users["user1json"]["auth_user_id"]
    })
    assert response.status_code == 403


def test_valid(users, channel):
    # this test testing valid output
    requests.post(config.url + "channels/create/v2", json={
        "token": users["user1json"]["token"],
        "name": "channel2",
        "is_public": True
    })
    response = requests.post(config.url + "channel/invite/v2", json={
        "token": users["user1json"]["token"],
        "channel_id": channel["channel_id"],
        "u_id": users["user2json"]["auth_user_id"]
    })
    assert response.status_code == 200
