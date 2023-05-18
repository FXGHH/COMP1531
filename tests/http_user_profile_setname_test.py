import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200


def test_user_profile_setname_with_invalid_token():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setname/v1',
                        json={'token': "wrong", 'name_first': 's', 'name_last': 's'})
    assert resp.status_code == 403


def test_user_profile_setname_with_invalid_first_name_1():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setname/v1',
                        json={'token': user_1['token'], 'name_first': '', 'name_last': 'test'})
    assert resp.status_code == 400


def test_user_profile_setname_with_invalid_first_name_2():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setname/v1', json={
                        'token': user_1['token'], 'name_first': 'abcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg', 'name_last': "test"})
    assert resp.status_code == 400


def test_user_profile_setname_with_invalid_last_name_1():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setname/v1',
                        json={'token': user_1['token'], 'name_first': 'test', 'name_last': ''})
    assert resp.status_code == 400


def test_user_profile_setname_with_invalid_last_name_2():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.put(config.url + 'user/profile/setname/v1', json={
                        'token': user_1['token'], 'name_first': 'test', 'name_last': 'abcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg'})
    assert resp.status_code == 400


def test_user_profile_setname_with_right_name():
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

    resp = requests.put(config.url + 'user/profile/setname/v1', json={
                        'token': user_2['token'], 'name_first': 'newfirstname', 'name_last': "newlastname"})
    assert resp.status_code == 200

    resp = requests.get(config.url + 'user/profile/v1',
                        params={'token': user_2['token'], 'u_id': 2})
    assert resp.status_code == 200
    assert resp.json() == {'user': {'u_id': 2, 'email': 'abcde@gmail.com', 'name_first': 'newfirstname',
                           'name_last': 'newlastname', 'handle_str': 'jake11renzella22'}}
