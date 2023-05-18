from src.data_store import data_store
from src.error import InputError, AccessError
import src.help as help
import re,os
import urllib.request
from PIL import Image
import uuid
from src import config

def users_all_v1(token):
    '''
    This function will take in token,
    and returns a list of all users and their associated details

    Args:
        token (string): the channel owner's token

    Exception:
        AccessError - when token is invalid

    Returns:
        {}
    '''
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    store = data_store.get()
    users_result = []
    for user in store['users']:
        if not user['removed']:
            user_result = {}
            user_result['u_id'] = user['auth_user_id']
            user_result['email'] = user['email']
            user_result['name_first'] = user['name_first']
            user_result['name_last'] = user['name_last']
            user_result['handle_str'] = user['handle']
            users_result.append(user_result)

    return {"users": users_result}


def user_profile_v1(token, u_id):
    '''
    This function will take in token and u_id,
    and returns the details about the users

    Args:
        token (string): the channel owner's token
        u_id (string): the u_id of the user

    Exception:
        InputError - u_id does not refer to a valid user
        AccessError - when token is invalid

    Returns:
        {}
    '''
    if not help.check_token(token):
        raise AccessError(description="Invalid token")

    if not help.check_u_id_valid(u_id):
        raise InputError("u_id does not refer to a valid user")

    find_user = help.searching_user_with_id(u_id)
    return_user = {}
    user_details = {}
    user_details['u_id'] = find_user['auth_user_id']
    user_details['email'] = find_user['email']
    user_details['name_first'] = find_user['name_first']
    user_details['name_last'] = find_user['name_last']
    user_details['handle_str'] = find_user['handle']
    user_details['handle_str'] = find_user['handle']
 
    return_user['user'] = user_details
    return return_user

def user_profile_v2(token, u_id):
    '''
    This function will take in token and u_id,
    and returns the details about the users

    Args:
        token (string): the channel owner's token
        u_id (string): the u_id of the user

    Exception:
        InputError - u_id does not refer to a valid user
        AccessError - when token is invalid

    Returns:
        {}
    '''
    if not help.check_token(token):
        raise AccessError(description="Invalid token")

    if not help.check_u_id_valid(u_id):
        raise InputError("u_id does not refer to a valid user")

    find_user = help.searching_user_with_id(u_id)
    return_user = {}
    user_details = {}
    user_details['u_id'] = find_user['auth_user_id']
    user_details['email'] = find_user['email']
    user_details['name_first'] = find_user['name_first']
    user_details['name_last'] = find_user['name_last']
    user_details['handle_str'] = find_user['handle']
    user_details['handle_str'] = find_user['handle']
    user_details['profile_img_url'] = "%s%s%s"%(config.url,config.image_save_path,find_user['profile_img'])

    return_user['user'] = user_details
    return return_user


def user_profile_setname_v1(token, name_first, name_last):
    '''
    This function will take in token name_frist and name_last,
    and update the authorised user's first and last name

    Args:
        token (string): the channel owner's token
        name_first (string): new first name
        name_last (string): new last name

    Exception:
        InputError - length of name_first is not between 1 and 50 characters inclusive
        InputError -length of name_last is not between 1 and 50 characters inclusive
        AccessError - when token is invalid

    Returns:
        {}
    '''

    if not help.check_token(token):
        raise AccessError(description="Invalid token")

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            "length of name_first is not between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            "length of name_last is not between 1 and 50 characters inclusive")

    store = data_store.get()
    for user in store["users"]:
        if token in user['token']:
            user['name_first'] = name_first
            user['name_last'] = name_last
    data_store.set(store)
    return {}


def user_profile_setemail_v1(token, email):
    '''
    This function will take in token and email,
    and update the authorised user's email

    Args:
        token (string): the channel owner's token
        email (string): new email

    Exception:
        InputError - email entered is not a valid email
        InputError - email address is already being used by another user
        AccessError - when token is invalid

    Returns:
        {}
    '''

    if not help.check_token(token):
        raise AccessError(description="Invalid token")

    # check does this is a valid email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if len(email) == 0 or re.fullmatch(regex, email) == None:
        raise InputError("Sorry, email entered is not a valid email")

    # check does the emial is or nor be register
    auth_user_id = help.get_auth_user_id(token)
    store = data_store.get()
    for user in store['users']:
        if user['email'] == email and auth_user_id != user['auth_user_id']:
            raise InputError(
                "email address is already being used by another user")

    for user in store["users"]:
        if token in user['token']:
            user['email'] = email
    data_store.set(store)
    return {}


def user_profile_sethandle_v1(token, handle_str):
    '''
    This function will take in token and handle_str,
    and update the authorised user's handle

    Args:
        token (string): the channel owner's token
        handle_str (string): new handle

    Exception:
        InputError - length of handle_str is not between 3 and 20 characters inclusive
        InputError - handle_str contains characters that are not alphanumeric
        InputError - the handle is already used by another user
        AccessError - when token is invalid

    Returns:
        {}
    '''

    if not help.check_token(token):
        raise AccessError(description="Invalid token")

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(
            "length of handle_str is not between 3 and 20 characters inclusive")

    if not handle_str.isalnum():
        raise InputError(
            "handle_str contains characters that are not alphanumeric")

    # check does the handle is or nor be used
    auth_user_id = help.get_auth_user_id(token)
    store = data_store.get()
    for user in store['users']:
        if user['handle'] == handle_str and auth_user_id != user['auth_user_id']:
            raise InputError("the handle is already used by another user")

    for user in store["users"]:
        if token in user['token']:
            user['handle'] = handle_str
    data_store.set(store)
    return {}


def user_profile_upload_photo_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
    This function will Given a URL of an image on the internet, 
    crops the image within bounds (x_start, y_start) and (x_end, y_end).
     Position (0,0) is the top left. Please note: 
     the URL needs to be a non-https URL (it should just have "http://" in the URL. We will only test with non-https URLs.

    Args:
        token (string): current user token
        img_url (string): image url
        x_start (int):
        y_start (int):
        x_end (int) :
        y_end (int) 

    Exception:
        img_url returns an HTTP status other than 200, or any other errors occur when attempting to retrieve the image
        any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL
        x_end is less than or equal to x_start or y_end is less than or equal to y_start
        image uploaded is not a JPG

    Returns:
        {}
    '''
    if not help.check_token(token):
        raise AccessError(description="Invalid token")

    if not os.path.exists(config.image_save_path):
        os.makedirs(config.image_save_path)
   
   
    # check does this is a valid email    
    if not img_url.startswith("http://"):
        raise InputError(description="img_url returns an HTTP status other than 200, or any other errors occur when attempting to retrieve the image")

    try:
        resp = urllib.request.urlopen(img_url)
        if resp.getcode() != 200:
            raise InputError(description="img_url returns an HTTP status other than 200, or any other errors occur when attempting to retrieve the image")
    except Exception as error:
        print(error)
        raise InputError(description="img_url returns an HTTP status other than 200, or any other errors occur when attempting to retrieve the image") from error

    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    image_name = "%s.jpg"%suid
    image_full_path = "%s%s"%(config.image_save_path,image_name)
    urllib.request.urlretrieve(img_url, image_full_path)
    imageObject = Image.open(image_full_path)

    if imageObject.format != "JPEG":
        raise InputError(description="image uploaded is not a JPG")
    
    width, height = imageObject.size
    if not ( x_start >= 0 and x_start < width
            and x_end >= 0 and x_end < width
            and y_start >= 0 and y_start < height
            and y_end >= 0 and y_end < height ):
        raise InputError(description="any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL")
    
    if x_end <= x_start or y_end <= y_start:
        raise InputError(description="x_end is less than or equal to x_start or y_end is less than or equal to y_start")
    
    croppedImage = imageObject.crop((x_start, y_start, x_end, y_end))
    croppedImage.save(image_full_path)
 
    store = data_store.get()
    for user in store["users"]:
        if token in user['token']:
            user["profile_img"] = image_name
    data_store.set(store)

    return {}