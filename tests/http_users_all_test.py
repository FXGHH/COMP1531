import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200


def test_users_all_with_invalid_token():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.get(config.url + 'users/all/v1', params={'token': "wrong"})
    assert resp.status_code == 403


def test_users_all_with_self():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.get(config.url + 'users/all/v1',
                        params={'token': user_1['token']})
    assert resp.status_code == 200
    assert resp.json() == {"users": [{"u_id": 1, "email": "abc@gmail.com",
                                      "name_first": "Jake", "name_last": "Renzella", "handle_str": "jakerenzella"}]}


def test_users_all_with_others():
    requests.delete(config.url + "/clear/v1")

    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    requests.post(config.url + "auth/register/v2", json={
        "email": "abcd@gmail.com",
        "password": "12345678",
        "name_first": "Jake1",
        "name_last": "Renzella2"
    }).json()

    user_3 = requests.post(config.url + "auth/register/v2", json={
        "email": "abcde@gmail.com",
        "password": "123456789",
        "name_first": "Jake11",
        "name_last": "Renzella22"
    }).json()

    resp = requests.get(config.url + 'users/all/v1',
                        params={'token': user_3['token']})
    assert resp.status_code == 200
    assert resp.json() == {"users": [{'u_id': 1, 'email': 'abc@gmail.com', 'name_first': 'Jake', 'name_last': 'Renzella', 'handle_str': 'jakerenzella'},
                           {'u_id': 2, 'email': 'abcd@gmail.com', 'name_first': 'Jake1',
                               'name_last': 'Renzella2', 'handle_str': 'jake1renzella2'},
                           {'u_id': 3, 'email': 'abcde@gmail.com', 'name_first': 'Jake11', 'name_last': 'Renzella22', 'handle_str': 'jake11renzella22'}]}
