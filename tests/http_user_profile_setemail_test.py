import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200


def test_user_profile_setemail_v1_with_invalid_token():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setemail/v1',
                        json={'token': "wrong", 'email': 's'})
    assert resp.status_code == 403


def test_user_profile_setemail_with_invalid_eamil_1():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setemail/v1',
                        json={'token': user_1['token'], 'email': ''})
    assert resp.status_code == 400


def test_user_profile_setemail_with_invalid_eamil_2():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setemail/v1',
                        json={'token': user_1['token'], 'email': 'test'})
    assert resp.status_code == 400


def test_user_profile_setemail_with_invalid_eamil_3():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setemail/v1',
                        json={'token': user_1['token'], 'email': 'test@122'})
    assert resp.status_code == 400


def test_user_profile_setemail_v1_with_already_use_email():
    requests.delete(config.url + "/clear/v1")

    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    user_2 = requests.post(config.url + "auth/register/v2", json={
        "email": "abcde@gmail.com",
        "password": "123456789",
        "name_first": "Jake11",
        "name_last": "Renzella22"
    }).json()

    resp = requests.put(config.url + 'user/profile/setemail/v1',
                        json={'token': user_2['token'], 'email': 'abc@gmail.com'})
    assert resp.status_code == 400


def test_user_profile_setemail_with_right_email():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    requests.post(config.url + "auth/register/v2", json={
        "email": "abcd@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    resp = requests.put(config.url + 'user/profile/setemail/v1',
                        json={'token': user_1['token'], 'email': 'test@163.com'})
    assert resp.status_code == 200

    resp = requests.get(config.url + 'user/profile/v1',
                        params={'token': user_1['token'], 'u_id': 1})
    assert resp.status_code == 200
    assert resp.json() == {'user': {'u_id': 1, 'email': 'test@163.com', 'name_first': 'Jake',
                           'name_last': 'Renzella', 'handle_str': 'jakerenzella'}}
