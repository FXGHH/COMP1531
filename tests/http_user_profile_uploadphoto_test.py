import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200

image_url = "http://pu.edu.pk/images/image/press/Jan-17/2(17-1-17).jpg"
def test_user_profile_uploadphoto_with_invalid_token():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    test_data ={'token': "wrong", 'img_url': image_url, 
        "x_start": 0,"y_start": 0,"x_end": 100,"y_end": 100}

    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 403


def test_user_profile_uploadphoto_wrong_size():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    expectedDefaultOutput= "%s%s%s"%(config.url,config.image_save_path, "default.jpg")
    resp = requests.get(config.url + 'user/profile/v2',
                        params={'token': user_1['token'], 'u_id': 1})
    assert resp.status_code == 200
    print(resp.json())
    assert resp.json()['user']['profile_img_url'] == expectedDefaultOutput 

    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 11110,"y_start": 0,"x_end": 30,"y_end": 30}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400

    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 0,"y_start": 11110,"x_end": 30,"y_end": 30}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400

    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 0,"y_start": 0,"x_end": 30333,"y_end": 30}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400

    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 0,"y_start": 0,"x_end": 30,"y_end": 3032}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400

    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 80,"y_start": 0,"x_end": 30,"y_end": 30}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400

    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 0,"y_start": 90,"x_end": 30,"y_end": 30}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400


def test_user_profile_uploadphoto_wrong_url_wrong_format():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    expectedDefaultOutput= "%s%s%s"%(config.url,config.image_save_path, "default.jpg")
    resp = requests.get(config.url + 'user/profile/v2',
                        params={'token': user_1['token'], 'u_id': 1})
    assert resp.status_code == 200
    print(resp.json())
    assert resp.json()['user']['profile_img_url'] == expectedDefaultOutput 
   
    test_data ={'token': user_1['token'], 'img_url': 'xxx', 
        "x_start": 0,"y_start": 0,"x_end": 50,"y_end": 50}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400

    test_data ={'token': user_1['token'], 'img_url': 'http://sdfds//sdfds', 
        "x_start": 0,"y_start": 0,"x_end": 50,"y_end": 50}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 400


def test_user_profile_uploadphoto_working():
    requests.delete(config.url + "/clear/v1")
    user_1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    expectedDefaultOutput= "%s%s%s"%(config.url,config.image_save_path, "default.jpg")
    resp = requests.get(config.url + 'user/profile/v2',
                        params={'token': user_1['token'], 'u_id': 1})
    assert resp.status_code == 200
    print(resp.json())
    assert resp.json()['user']['profile_img_url'] == expectedDefaultOutput 
   
    
    test_data ={'token': user_1['token'], 'img_url': image_url, 
        "x_start": 0,"y_start": 0,"x_end": 100,"y_end": 100}
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1',json=test_data)
    assert resp.status_code == 200

    resp = requests.get(config.url + 'user/profile/v2',
                        params={'token': user_1['token'], 'u_id': 1})
    assert resp.status_code == 200
    
    print(resp.json())
    assert resp.json()['user']['profile_img_url'] != expectedDefaultOutput 


 