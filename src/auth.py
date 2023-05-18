from src.data_store import data_store
from src.error import InputError, AccessError
import sys
import re
import src.help as help
import random


def auth_login_v2(email, password):
    '''
    This function will take in email, password
    login the user, and give back a new token and the user id

    Args:
        email (string): user email
        password (string): user password
    
    Exception:
        InputError when any of:
        1. email entered does not belong to a user
        2. password is not correct

    Returns:
        {'token': xxx, 'auth_user_id': xxx}
    '''
    # get data
    store = data_store.get()
    for user in store["users"]:
        # check if the email is in the data store and is not the removed user
        if user["email"] == email and user['removed'] == False:
            if user["password"] == help.hash(password):
                # generate new session id and new token, return the new token and user id in a new dictionary
                session_id = help.generate_new_session_id()
                user['session_id'].append(session_id)
                new_token = help.generate_jwt(user['auth_user_id'], session_id)
                user['token'].append(new_token)
                data_store.set(store)
                return {'token': new_token, 'auth_user_id': user["auth_user_id"]}
            # check if the password is correct
            else:
                raise InputError(description="Sorry, the password is not correct, please try again")
    # check if the email is valid
    raise InputError(description="Sorry, the email entered does not belong to a user")


def auth_logout_v1(token):
    '''
    This function will take in token
    logout the user by removing authorised token
    
    Args:
        token (string): authorised token

    Exception:
        AccessError:
        1. invalid token

    Returns:
        {}
    '''
    # check if the authorised token valid and decode the token to get authorised user id
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    auth_user_id = help.get_auth_user_id(token)
    
    # get data
    store = data_store.get()
    
    # get user details and remove the token
    user = help.get_user_with_auth_user_id(auth_user_id)
    user['token'].remove(token)
    data_store.set(store)
    return {}

def auth_register_v2(email, password, name_first, name_last):
    '''
    This function will take in email, password, name_first, name_last
    auth_register_v2 the user, and give back a new token and the user id

    Args:
        email (string): user email
        password (string): user password
        name_first (string):user name_first
        name_last (string):user name_first

    Exceptions:
        InputError: email entered is not a valid email
        InputError: email address is already being used by another user
        InputError: length of password is less than 6 characters
        InputError: length of name_first is not between 1 and 50 characters inclusive
        InputError: length of name_last is not between 1 and 50 characters inclusive
    Returns:
        {'token': xxx, 'auth_user_id': xxx}
    '''
    ##########################################################
    # get data
    store = data_store.get()

    # check does this is a valid email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if re.fullmatch(regex, email) == None:
        raise InputError(description="Sorry, email entered is not a valid email")

    # check does the emial is or nor be register
    if len(store['users']) > 0:
        for user in store['users']:
            if user['email'] == email and user["removed"] == False:
                raise InputError(
                    description="email address is already being used by another user")

    # check the length of password, firsr name last name
    if len(password) < 6:
        raise InputError(description="Sorry, length of password is less than 6 characters")
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError(
            description="Sorry, length of name_first is not between 1 and 50 characters inclusive")
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError(
            description="Sorry, length of name_last is not between 1 and 50 characters inclusive")

    # new dic for add to datastore initial_object["users"]
    new_dc = {}

    # handle
    lower_case_name_first = name_first.lower()
    lower_case_name_last = name_last.lower()
    handle = lower_case_name_first + '' + lower_case_name_last
    # it1 test_handles_generated_correctly fix
    handle = ''.join(filter(str.isalnum, handle))
    if len(handle) > 20:
        handle = handle[:20]
    # check how many same handle without number in data_store
    number_han_exsit = 0
    for exsit in store['users']:
        handle_in_data = exsit["handle"]
        handle_no_number = handle_in_data[:len(handle)]
        if handle_no_number == handle:
            number_han_exsit = number_han_exsit + 1
    # when no same handle in data, insert this handle to dic, like handle
    if number_han_exsit == 0:
        new_dc['handle'] = handle
        # if only one same handle, insert this handle + a string zero, like handle0
    elif number_han_exsit == 1:
        handle = handle + '' + '0'
        new_dc['handle'] = handle
        # otherwith return the number minus 1, for example there are two same handle
        # "handle" and "handle0", total handle = 2, but the new handle is "handle1"
    else:
        handle = handle + '' + str(number_han_exsit - 1)
        new_dc['handle'] = handle

    # new_id
    # new_id = len(store['users']) + 1
    new_id = store['total_users'] + 1
    store['total_users'] += 1

    # global owner fix
    if new_id == 1:
        new_dc['is_global_owner'] = True
    else:
        new_dc['is_global_owner'] = False


    # session id and token
    session_id = help.generate_new_session_id()
    new_token = help.generate_jwt(new_id, session_id)

    session_id_list = []
    token_list = []

    session_id_list.append(session_id)
    token_list.append(new_token)
    # store all details to datastore
    new_dc['email'] = email
    new_dc['auth_user_id'] = new_id
    new_dc['password'] = help.hash(password)  # password hash
    new_dc['name_first'] = name_first
    new_dc['name_last'] = name_last
    new_dc['session_id'] = session_id_list      # session ids
    new_dc['token'] = token_list            # tokens
    new_dc['removed'] = False              
    new_dc['notifications'] = []            #notifications
    #For any given user, if they have yet to upload an image, there should be a site-wide default image used.
    new_dc['profile_img'] = 'default.jpg'
 
    new_dc['user_stats'] = { 'channels_joined': [],'dms_joined': [], 'messages_sent': []}

    #For users, the first data point should be 0 for all metrics at the time that their account was created
    channels_joined = {
        "num_channels_joined": 0,
        "time_stamp": help.get_current_time_stamp()
    }
    new_dc['user_stats']['channels_joined'].append(channels_joined)

    dms_joined = {
        "num_dms_joined": 0,
        "time_stamp": help.get_current_time_stamp(),
    }
    new_dc['user_stats']['dms_joined'].append(dms_joined)

    messages_sent = {
        "num_messages_sent": 0,
        "time_stamp": help.get_current_time_stamp(),
    }
    new_dc['user_stats']['messages_sent'].append(messages_sent)
    new_dc['reset_code'] = ""
 
    store['users'].append(new_dc)


    if len(store['users']) == 1:
        channels_exist = {
            "num_channels_exist": 0,
            "time_stamp": help.get_current_time_stamp()
        }
        store['workspace_stats']['channels_exist'].append(channels_exist)

        dms_exist = {
            "num_dms_exist": 0,
            "time_stamp": help.get_current_time_stamp(),
        }
        store['workspace_stats']['dms_exist'].append(dms_exist)

        messages_exist = {
            "num_messages_exist": 0,
            "time_stamp": help.get_current_time_stamp(),
        }
        store['workspace_stats']['messages_exist'].append(messages_exist)

    data_store.set(store)
    
    return {
        'token': new_token,
        'auth_user_id': new_id
    }

def auth_passwordreset_request_v1(email):
    '''
    Given an email address, if the user is a registered user,
    sends them an email containing a specific secret code, that when entered in auth/passwordreset/reset,
    shows that the user trying to reset the password is the one who got sent this email.
    No error should be raised when passed an invalid email, as that would pose a security/privacy concern.
    When a user requests a password reset, they should be logged out of all current sessions.

    Args:
        email (string): user email

    Exceptions:
        None
    Returns:
        {}
    '''
    store = data_store.get()
    reset_code = str(random.randint(100000, 999999))
    for user in store['users']:
        if user['email'] == email:
            user['reset_code'] = reset_code
    data_store.set(store)
    return {}

def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password provided.
    Once a reset code has been used, it is then invalidated.
    Args:
        reset_code: the code get form the email of user.
        new_password: the new password user input.

    Exceptions:
        InputError: reset_code is not a valid reset code
        InputError: password entered is less than 6 characters long
    Returns:
        {}
    '''
    store = data_store.get()
    correct_reset_code = False
    for user in store["users"]:
        if reset_code == user["reset_code"]:
            correct_reset_code = True
    
    if correct_reset_code == False:
        raise InputError(description="reset_code is not a valid reset code")
    if len(new_password) < 6:
        raise InputError(description="password entered is less than 6 characters long")

    for dic in store["users"]:
        if dic["reset_code"] == reset_code:
            dic["password"] = help.hash(new_password)
            dic["reset_code"] = ""

    data_store.set(store)
    return {}
