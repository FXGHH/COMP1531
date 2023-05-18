import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200


def test_user_profile_with_invalid_token():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.get(config.url + 'user/profile/v1',
                        params={'token': "wrong", 'u_id': 1})
    assert resp.status_code == 403


def test_user_profile_with_invalid_user():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.get(config.url + 'user/profile/v1',
                        params={'token': user_1['token'], 'u_id': 234})
    assert resp.status_code == 400


def test_user_profile_with_right_others():
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

    resp = requests.get(config.url + 'user/profile/v1',
                        params={'token': user_3['token'], 'u_id': 1})
    assert resp.status_code == 200
    assert resp.json() == {'user': {'u_id': 1, 'email': 'abc@gmail.com',
                                    'name_first': 'Jake', 'name_last': 'Renzella', 'handle_str': 'jakerenzella'}}
