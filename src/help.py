import hashlib
import jwt
import json
import datetime
from src.data_store import data_store
import re

SESSION_TRACKER = 0
SECRET = 'F13B_ELEPHANT'


def generate_new_session_id():
    """
    This function will generate a new session id

    Returns:
        the latest session id
    """
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return SESSION_TRACKER


def hash(string):
    """
    This function will encode the password

    Args:
        password(string)
    Returns:
        the hash password
    """
    return hashlib.sha256(string.encode()).hexdigest()


def generate_jwt(auth_user_id, session_id):
    """
    This function will generate an encoded jwt with given uid, session id, and secret

    Args:
        u_id(int)
        session_id(int)
        secret(string): 'HS256'
    Returns:
        an encoded jwt
    """
    return jwt.encode({'auth_user_id': auth_user_id, 'session_id': session_id}, SECRET, algorithm='HS256')


def decode_jwt(encoded_jwt):
    """
    This function will decode an encoded jwt 

    Args:
        encoded_jwt(string)
    Returns:
        {'auth_user_id': xxx, 'session_id': xxx}
    """
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])


def get_auth_user_id(token):
    """
    This function will decode an encoded jwt to get a corresponding uid

    Args:
        encoded_jwt(string)
    Returns:
        auth_user_id(int)
    """
    data = decode_jwt(token)
    return data['auth_user_id']


# def get_session_id(token):
#     data = decode_jwt(token)
#     return data['session_id']


def check_token(token):
    """
    This function will check if the token given is exist in the data store
    Args:
        encoded_jwt(string)
    Returns:
        True/False
    """
    store = data_store.get()
    is_ok = False
    for user in store['users']:
        if token in user['token']:
            is_ok = True
    return is_ok


# def check_session_id(token):
#     auth_user_id = get_auth_user_id(token)
#     session_id = get_session_id(token)
#     store = data_store.get()
#     is_ok = False
#     for user in store['users']:
#         if auth_user_id == user['auth_user_id'] and session_id in user['session_id']:
#             is_ok = True
#     return is_ok

def get_user_with_auth_user_id(auth_user_id):
    """
    This function will search the user with the uid

    Args:
        uid(int)
    Returns:
        user detail dictionary
    """
    store = data_store.get()
    userget = {}
    for user in store['users']:
        if auth_user_id == user['auth_user_id']:
            userget = user
    return userget


def save_data():
    """
    This function will save the data in the server
    """
    store = data_store.get()
    with open("store.json", "w") as FILE:
        FILE.write(json.dumps(store))


def check_auth_user_id_valid(auth_user_id):
    '''
    This fucntion to check
    whether the auth_user_id have been created or not
    '''
    valid_auth_user_id = False
    store = data_store.get()
    for user in store["users"]:
        if int(user["auth_user_id"]) == auth_user_id:
            valid_auth_user_id = True
            return valid_auth_user_id
    return valid_auth_user_id


def check_channel_id_valid(channel_id):
    '''
    This function to check
    whether the channel_id have been created or not
    '''
    valid_channel_id = False
    store = data_store.get()
    for channel in store["channels"]:
        if int(channel["channel_id"]) == channel_id:
            valid_channel_id = True
            return valid_channel_id
    return valid_channel_id


def check_u_id_valid(u_id):
    '''
    This function to check
    whether the user with u_id have regesited or not
    '''
    valid_u_id = False
    store = data_store.get()
    for user in store["users"]:
        if int(user["auth_user_id"]) == u_id:
            valid_u_id = True
            return valid_u_id
    return valid_u_id


def check_u_id_in_the_channel(u_id, ch_id):
    '''
    This function to check
    whether the user with u_id is already in the channel or not
    '''
    u_id_in_the_channel = False
    store = data_store.get()
    for invitee in store["channels"]:
        if ch_id == invitee["channel_id"]:
            if u_id in invitee["auth_user_id"] or u_id in invitee["channel_user_id"]:
                u_id_in_the_channel = True
                return u_id_in_the_channel
    return u_id_in_the_channel


def check_token_valid(token):
    '''
    This fucntion to check
    whether the user with token have already login or not
    '''
    valid_token = False
    store = data_store.get()
    for user in store["users"]:
        if token in user["token"]:
            valid_token = True
            return valid_token
    return valid_token


def get_user_with_token(token):
    '''
    This fucntion to return
    auth_user_id with input token
    '''
    store = data_store.get()
    for user in store["users"]:
        if token in user["token"]:
            auth_user_id = user["auth_user_id"]

    return auth_user_id


def check_uid_is_owner(u_id, channel_id):
    '''
    This fucntion to check if the uid is in the owner list of the channel
    '''
    valid_owner = False
    channel = searching_channel_with_channel_id(channel_id)
    if u_id in channel['auth_user_id']:
        valid_owner = True
        return valid_owner
    return valid_owner

def check_uid_has_owner_permission(u_id, channel_id):
    '''
    This fucntion to check if the uid is in the owner permission list of the channel
    '''
    valid_owner_permission = False
    channel = searching_channel_with_channel_id(channel_id)
    if u_id in channel['owner_permission']:
        valid_owner_permission = True
        return valid_owner_permission
    return valid_owner_permission

def check_uid_is_member(u_id, channel_id):
    '''
    This fucntion to check if the uid is in the member list of the channel
    '''
    valid_member = False
    channel = searching_channel_with_channel_id(channel_id)
    if u_id in channel['channel_user_id']:
        valid_member = True
    return valid_member


def searching_user_with_id(u_id):
    """
    This function will take in an user_id and give back the details
    of the user

    Args:
        u_id (int): input the u_id and give back the user detail

    Returns:
        user_details (dict): User's details
    """
    store = data_store.get()
    return_user_details = {}
    for user in store["users"]:
        if u_id == user["auth_user_id"]:
            return_user_details = user

    return return_user_details


def searching_channel_with_channel_id(channel_id):
    """
    This function will take in a channel_id and give back the details
    of the channel

    Args:
        channel_id (int): input the channel_id and give back the user detail

    Returns:
        user_details (dict): User's details
    """
    return_channel = {}
    store = data_store.get()
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            return_channel = channel
    return return_channel


def dm_id_is_valid(dm_id):
    """
    This function will check if the given dm_id is exist in the data store

    Args:
        dm_id (int)

    Returns:
        True/False
    """
    store = data_store.get()
    valid_dm_id = False
    for id in store["dm"]:
        if dm_id == id["dm_id"]:
            valid_dm_id = True
    return valid_dm_id


def uid_in_dm(auth_user_id):
    """
    This function will check if the given uid is in any of the dm

    Args:
        u_id (int)

    Returns:
        True/False
    """
    store = data_store.get()
    uid_in_dm = False
    for id in store["dm"]:
        if auth_user_id in id["dm_members_id"]:
            uid_in_dm = True
    return uid_in_dm


def find_channel_by_message_id(message_id):
    """
    This function will take message_id and give back the channel dic

    Args:
        message_id (int): unique message ID

    Returns:
        channel_dic (dict): channel dic
    """
    channel_dic = {}
    store = data_store.get()
    for channel in store["channels"]:
        for message in channel["message"]:
            if message["message_id"] == message_id:
                channel_dic = channel
    return channel_dic


def find_dm_by_message_id(message_id):
    """
    This function will take message_id and give back the channel dic

    Args:
        message_id (int): unique message ID

    Returns:
        channel_dic (dict): channel dic
    """
    channel_dic = {}
    store = data_store.get()
    for dm in store["dm"]:
        for message in dm["dm_messages"]:
            if message["message_id"] == message_id:
                channel_dic = dm
                return channel_dic
    return channel_dic


def message_id_is_valid_in_channel(message_id):
    """
    This function will take message_id and response the message id is valid or not(in channel )

    Args:
        message_id (int): unique message ID

    Returns:
        message_exit (int): does it exit
    """
    message_exit = False
    store = data_store.get()
    for channel in store["channels"]:
        for message in channel["message"]:
            if message["message_id"] == message_id:
                message_exit = True
    return message_exit


def message_id_is_valid_in_dm(message_id):
    """
    This function will take message_id and response the message id is valid or not(in dm)

    Args:
        message_id (int): unique message ID

    Returns:
        message_exit (int): does it exit
    """
    message_exit = False
    store = data_store.get()
    for channel in store['dm']:
        for message in channel['dm_messages']:
            if message["message_id"] == message_id:
                message_exit = True
    return message_exit


def find_message_in_channel(message_id):
    """
    This function will take message_id and give back the message dic

    Args:
        message_id (int): unique message ID

    Returns:
        message_dic (dict): messaeg dic
    """
    message_dic = {}
    store = data_store.get()
    for channel in store["channels"]:
        for message in channel["message"]:
            if message["message_id"] == message_id:
                message_dic = message
    return message_dic


def find_message_in_dm(message_id):
    """
    This function will take message_id and give back the message dic

    Args:
        message_id (int): unique message ID

    Returns:
        message_dic (dict): messaeg dic
    """
    message_dic = {}
    store = data_store.get()
    for dm in store["dm"]:
        for message in dm['dm_messages']:
            if message["message_id"] == message_id:
                message_dic = message
                return message_dic
    return message_dic


def check_dm_id_valid(dm_id):
    '''
    This function to check
    whether the channel_id have been created or not
    '''
    valid_dm_id = False
    store = data_store.get()
    for dm in store["dm"]:
        if int(dm["dm_id"]) == dm_id:
            valid_dm_id = True
            return valid_dm_id
    return valid_dm_id


def check_u_id_in_the_dm(u_id):
    """
    This function will take in a u_id and give back True or False as the result of 
    whether the user is in the dm

    Args:
        u_id (int): input the u_id and give back Ture or False

    Returns:
        status (bool): True or False
    """
    u_id_in_the_dm = False
    store = data_store.get()
    for user in store["dm"]:
        if u_id in user["dm_members_id"]:
            u_id_in_the_dm = True
            return u_id_in_the_dm
    return u_id_in_the_dm


def get_user_details(u_id):
    """
    This function will take in a u_id and give back the details of the users

    Args:
        u_id (int): input the u_id and give back Ture or False

    Returns:
        user_details (dict): user's details
    """
    store = data_store.get()
    user_details = {}
    for user in store["users"]:
        if u_id == user["auth_user_id"]:
            user_details["u_id"] = user["auth_user_id"]
            user_details["email"] = user["email"]
            user_details["name_first"] = user["name_first"]
            user_details["name_last"] = user["name_last"]
            user_details["handle_str"] = user["handle"]
    return user_details


def searching_dm_with_dm_id(dm_id):
    """
    This function will take in a dm_id and give back the details
    of the dm

    Args:
        dm_id (int): input the dm_id and give back the user detail

    Returns:
        dm_details (dict): details about dm
    """
    return_dm = {}
    store = data_store.get()
    for dm in store["dm"]:
        if dm["dm_id"] == dm_id:
            return_dm = dm
    return return_dm


def change_removed_user_messages(u_id):
    """
    This function will replace all the messages sent by uid with 'Removed user' in channels and dms

    Args:
        u_id (int)

    """
    store = data_store.get()
    for channel in store["channels"]:
        for message in channel["message"]:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'

    for dm in store["dm"]:
        for message in dm['dm_messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
    data_store.set(store)
    return


def add_uid_to_channel_owner(u_id):
    """
    This function will add the uid to the channels owner list

    Args:
        u_id (int)

    """
    store = data_store.get()
    for dic in store['channels']:
        if u_id in dic['channel_user_id'] and u_id not in dic['owner_permission']:
            dic['owner_permission'].append(u_id)
    data_store.set(store)
    return


def remove_uid_from_channel_owner(u_id):
    """
    This function will remove the uid from the channels owner list

    Args:
        u_id (int)

    """
    store = data_store.get()
    for dic in store['channels']:
        if u_id not in dic['auth_user_id'] and u_id != dic['channel_creator'] and u_id in dic['owner_permission']:
            dic['owner_permission'].remove(u_id)
    data_store.set(store)
    return

def check_standup_active(channel_id):
    """
    This function will check if a standup is actived in target channel

    Args:
        channel_id (int)

    """
    store = data_store.get()
    standup_active = False
    for dic in store['standups']:
        if dic['channel_id'] == channel_id:
            standup_active = True
            return standup_active
    return standup_active


def get_current_time_stamp():
    """
    This function will get current time stamp
    Returns:
        current time stamp
    """
    return int(datetime.datetime.now().timestamp()*1000)

def get_sum_for_user_stats():
    """
    This function will get sum(num_channels, num_dms, num_msgs)

    Args:
        NONE
    Returns:
        sum(num_channels, num_dms, num_msgs)
    """
    
    store = data_store.get()
    #print(store)
    messages_number = 0
    for channel in store['channels']:
        messages_number = len(channel['message']) + messages_number

    for dm in store['dm']:
        messages_number = len(dm['dm_messages']) + messages_number

    return len(store['channels']) + len(store['dm']) + messages_number
 
 
def get_user_num_for_users_stats():
    """
    This function will num users who have joined at least one channel or dm

    Args:
        NONE
    Returns:
        num users who have joined at least one channel or dm
    """
    store = data_store.get()
    messages_number = 0
    for channel in store['channels']:
        messages_number = len(channel['message']) + messages_number

    for dm in store['dm']:
        messages_number = len(dm['dm_messages']) + messages_number

    return len(store['channels']) + len(store['dm']) + messages_number


def update_num_channels_joined(u_id, is_increase):
    """
    This function will take in an user_id and increase or decrease the user joined num channels
    of the user

    Args:
        u_id (int): input the u_id  

    Returns:
        NULL
    """
    store = data_store.get()
    for user in store["users"]:
        if u_id == user["auth_user_id"]:
            channels_joined_list = user['user_stats']['channels_joined']
            if len(channels_joined_list) > 0:
                latest_channels_joined = channels_joined_list[-1]
                latest_num_channels_joined = latest_channels_joined['num_channels_joined']
                change = 1 if is_increase else -1
                new_channels_joined = {
                    "num_channels_joined": latest_num_channels_joined + change,
                    "time_stamp": get_current_time_stamp()
                }
                user['user_stats']['channels_joined'].append(new_channels_joined)
            break
    data_store.set(store)


def update_num_dms_joined(u_id,is_increase):
    """
    This function will take in an user_id and increase the user joined dm
    of the user

    Args:
        u_id (int): input the u_id  

    Returns:
        NULL
    """
    store = data_store.get() 
    for user in store["users"]: 
        if u_id == user["auth_user_id"]:
            dms_joined_list = user['user_stats']['dms_joined']
            if len(dms_joined_list) > 0:
                latest_dms_joined  = dms_joined_list[-1]
                latest_num_dms_joined = latest_dms_joined['num_dms_joined']
                change = 1 if is_increase else -1
                new_dms_joined = {
                    "num_dms_joined": latest_num_dms_joined + change,
                    "time_stamp": get_current_time_stamp()
                }
                user['user_stats']['dms_joined'].append(new_dms_joined)
            break       
    data_store.set(store)

def update_num_messages_sent(u_id):
    """
    the number of messages sent will only increase

    Args:
        u_id (int): input the u_id  

    Returns:
        NULL
    """
    store = data_store.get()
    for user in store["users"]:
        if u_id == user["auth_user_id"]:
            messages_sent_list = user['user_stats']['messages_sent']
            if len(messages_sent_list) > 0:
                latest_messages_sent  = messages_sent_list[-1]
                latest_num_messages_sent = latest_messages_sent['num_messages_sent']
                new_messages_sent = {
                    "num_messages_sent": latest_num_messages_sent + 1,
                    "time_stamp": get_current_time_stamp()
                }
                user['user_stats']['messages_sent'].append(new_messages_sent)
            break
    data_store.set(store)


def update_channels_exist():
    """
   num_channels will never decrease as there is no way to remove channels,

    Args:  
        NULL
    Returns:
        NULL
    """
    store = data_store.get()
 
    current_list = store['workspace_stats']['channels_exist']
    if len(current_list) > 0:
        latest_object  = current_list[-1]
        latest_num = latest_object['num_channels_exist']
        new_object = {
            "num_channels_exist": latest_num + 1,
            "time_stamp": get_current_time_stamp()
        }
        store['workspace_stats']['channels_exist'].append(new_object)

    data_store.set(store)


def update_dms_exist(is_increase):
    """
    num_dms will only decrease when dm/remove is called.

    Args:  
        NULL
    Returns:
        NULL
    """
    store = data_store.get()
 
    current_list = store['workspace_stats']['dms_exist']
    if len(current_list) > 0:
        latest_object  = current_list[-1]
        latest_num = latest_object['num_dms_exist']
        change = 1 if is_increase else -1
        new_object = {
            "num_dms_exist": latest_num + change,
            "time_stamp": get_current_time_stamp()
        }
        store['workspace_stats']['dms_exist'].append(new_object)

    data_store.set(store)


def update_messages_exist(is_increase):
    """
   num_dms will only decrease when dm/remove is called.

    Args:  
        NULL
    Returns:
        NULL
    """
    store = data_store.get()
 
    current_list = store['workspace_stats']['messages_exist']
    if len(current_list) > 0:
        latest_object  = current_list[-1]
        latest_num = latest_object['num_messages_exist']
        change = 1 if is_increase else -1
        new_object = {
            "num_messages_exist": latest_num + change,
            "time_stamp": get_current_time_stamp()
        }
        store['workspace_stats']['messages_exist'].append(new_object)

    data_store.set(store)

def get_user_handle(auth_user_id):
    """
    get user handle

    Args:  
        NULL
    Returns:
        handle
    """
    store = data_store.get()
    handle = ''
    for user in store["users"]:
        if user["auth_user_id"] == auth_user_id:
            handle = user["handle"]
    return handle

def get_channel_name(channel_id):
    """
    get channel name

    Args:  
        NULL
    Returns:
        channel_name
    """
    store = data_store.get()
    channel_name = ''
    for ch in store["channels"]:
        if ch["channel_id"] == channel_id:
            channel_name = ch["channel_name"]
    return channel_name

def get_dm_name(dm_id):
    """
    get dm name

    Args:  
        NULL
    Returns:
        dm_name
    """
    store = data_store.get()
    dm_name = ''
    for dm in store["dm"]:
        if dm["dm_id"] == dm_id:
            dm_name = dm["dm_name"]
    return dm_name

def get_message_tagged_list(message):
    """
    get tagged handle

    Args:  
        NULL
    Returns:
        final_list
    """
    list_message = message.split()
    list_tagged = []
    for item in list_message:
        if item.find("@") != -1:
            list_tagged.append(item)

    tagged_str = ''
    for tag in list_tagged:
        tagged_str += '' + tag
    
    result_list = tagged_str.split("@")
    final_list = []
    for i in result_list:
        c = re.sub(r'[^\w\s]','',i)
        final_list.append(c)

    return final_list