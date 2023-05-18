from urllib import response
import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
@pytest.fixture
def user():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    })
    return user.json()

def test_auth_logout_invalid_token():
    requests.delete(config.url + '/clear/v1')
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': 'abc'})
    assert response.status_code == 403

def test_auth_logout_incorrect_token(user):
    requests.post(config.url + 'auth/logout/v1', json = {'token': user['token']})
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': user['token']})
    assert response.status_code == 403

def test_auth_logout_is_work_1(user):
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': user['token']})
    assert response.status_code == OK_STATUS

def test_auth_logout_is_work_2(user):
    login = requests.post(config.url + 'auth/login/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
    }).json() 
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': login['token']})
    assert response.status_code == OK_STATUS

def test_auth_logout_is_work_3(user):
    login = requests.post(config.url + 'auth/login/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
    }).json() 
    requests.post(config.url + 'auth/logout/v1', json = {'token': user['token']})
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': user['token']})
    assert response.status_code == 403
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': login['token']})
    assert response.status_code == OK_STATUS

def test_auth_logout_is_work_4(user):
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abcd@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    response = requests.post(config.url + 'auth/logout/v1', json = {'token': user2['token']})
    assert response.status_code == OK_STATUS
