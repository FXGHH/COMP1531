from distutils.command.config import config
import pytest
from src.auth import auth_register_v2
from src.user_profile import user_profile_v2, user_profile_upload_photo_v1
from src import config
from src.other import clear_v1
from src.error import AccessError, InputError

image_url = "http://pu.edu.pk/images/image/press/Jan-17/2(17-1-17).jpg"

def test_user_profile_uploadphoto_with_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        user_profile_upload_photo_v1( "token", image_url, 0, 0, 100, 100)

def test_user_profile_uploadphoto_wrong_size():
    clear_v1() 
    user1 = auth_register_v2("xxxx@hotmail.com", "1211321", "name1", "name12")
    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], image_url, 10000, 0, 30, 30)

    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], image_url, 0, 10000, 30, 30)

    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], image_url, 0, 0, 30000, 30)

    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], image_url, 0, 0, 30, 300000)

    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], image_url, 50, 0, 30, 30)
    
    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], image_url, 0, 50, 30, 30)

def test_user_profile_uploadphoto_wrong_url_wrong_format():
    clear_v1() 
    user1 = auth_register_v2("xxxx@hotmail.com", "1211321", "name1", "name12")
    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], "error", 0, 0, 20, 20)

    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], "http://wxsdf.com/sdfds", 0, 0, 20, 20)
    
    with pytest.raises(InputError):
        user_profile_upload_photo_v1(user1["token"], "https://wxsdf.com/sdfds", 0, 0, 20, 20)


def test_user_profile_uploadphoto_working():
    clear_v1()
    user1 = auth_register_v2("xxxx@hotmail.com", "1211321", "name1", "name12")
 
    userProfile = user_profile_v2(user1["token"], user1["auth_user_id"])
    expectedDefaultOutput= "%s%s%s"%(config.url,config.image_save_path, "default.jpg")
   
    print(userProfile)
    assert userProfile['user']['profile_img_url'] == expectedDefaultOutput 
    
    user_profile_upload_photo_v1(user1["token"], image_url, 0, 0, 100, 100)
    userProfile = user_profile_v2(user1["token"], user1["auth_user_id"])
    assert userProfile['user']['profile_img_url'] != expectedDefaultOutput 
 
 
 