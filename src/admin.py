from src.data_store import data_store
from src.error import InputError, AccessError
import sys
import re
import src.help as help

def admin_user_remove_v1(token, u_id):
    '''
    This function will take in token, u_id
    remove the user from all the channels and dms, replace the message by 'Removed user', replace the user's first name and last name by 'Removed'
    and 'user' seperately

    Args:
        token (string): authorised user token
        uid (int): target user
    
    Exception:
        InputError when any of:
        1. u_id does not refer to a valid user
        2. u_id refers to a user who is the only global owner
      
        AccessError when:
        1. the authorised user is not a global owner
        2. invalid token
        
    Returns:
        {}
    '''
    # get data
    store = data_store.get()
    
    # check authorised token valid
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    
    # get authorised user id by decoding token
    auth_user_id = help.get_auth_user_id(token)
    
    # check the authorised user is global owner
    is_global_owner = False
    for dic in store['users']:
        if dic["auth_user_id"] == auth_user_id:
            if dic['is_global_owner'] == True:
                is_global_owner = True
    if is_global_owner == False:
        raise AccessError(description='the authorised user is not a global owner')
    
    # check if uid is valid
    if help.check_u_id_valid(u_id) == False:
        raise InputError(description='uid does not refer to a valid user')
    
    # check if the target uid is the only global owner
    global_owner_num = 0
    for dic in store['users']:
        if dic['is_global_owner'] == True:
            global_owner_num += 1
    if global_owner_num == 1 and auth_user_id == u_id:
        raise InputError(description='uid refers to a user who is the only global owner')
    
    # remove target uid from all channels
    for dic in store['channels']:
        if u_id in dic['auth_user_id']:
            dic['auth_user_id'].remove(u_id)
        if u_id in dic['channel_user_id']:
            dic['channel_user_id'].remove(u_id)
        if u_id in dic['owner_permission']:
            dic['owner_permission'].remove(u_id)
    
    # remove target uid from all dms
    for dic in store['dm']:
        if u_id in dic['dm_creator_id']:
            dic['dm_creator_id'].remove(u_id)
        if u_id in dic['dm_members_id']:
            dic['dm_members_id'].remove(u_id)
    
    # replace the removed user's first name with 'Removed' and last name with 'user'
    for dic in store['users']:
        if dic['auth_user_id'] == u_id:
            dic['removed'] = True
            dic['name_first'] = 'Removed'
            dic['name_last'] = 'user'
            dic['token'].clear()
    
    # replace all the messages the uid sent with 'Removed user'
    help.change_removed_user_messages(u_id)
    
    # save data
    data_store.set(store)
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    This function will take in token, u_id, permission_id
    change the user permission of seams

    Args:
        token (string): authorised user token
        uid (int): target user
        permission_id(int): 1 or 2

    Exception:
        InputError when any of:     
        1. u_id does not refer to a valid user
        2. u_id refers to a user who is the only global owner and they are being demoted to a user
        3. permission_id is invalid
        4. the user already has the permissions level of permission_id
      
      AccessError when:
        1. the authorised user is not a global owner
        2. token invalid
        
    Returns:
        {}
    '''
    # get data
    store = data_store.get()
    
    # check authorised token valid
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')

    # get authorised user id by decoding token
    auth_user_id = help.get_auth_user_id(token)
    
    # check if the authorised user is global owner
    is_global_owner = False
    for dic in store['users']:
        if dic["auth_user_id"] == auth_user_id:
            if dic['is_global_owner'] == True:
                is_global_owner = True
    if is_global_owner == False:
        raise AccessError(description='the authorised user is not a global owner')
    
    # check if the target uid is valid
    if help.check_u_id_valid(u_id) == False:
        raise InputError(description='uid does not refer to a valid user')
    
    # check permission id is valid
    if permission_id != 1 and permission_id != 2:
        raise InputError(description='permission id is invalid')
    
    # check if the target user already had the permission of given permission id
    for dic in store['users']:
        if dic['auth_user_id'] == u_id:
            if (dic['is_global_owner'] == True and permission_id == 1) or (dic['is_global_owner'] == False and permission_id == 2):
                raise InputError(description='the user already has the permissions level of permission id')
    
    # check if the target uid is the only global owner
    global_owner_num = 0
    for dic in store['users']:
        if dic['is_global_owner'] == True:
            global_owner_num += 1
    if global_owner_num == 1 and auth_user_id == u_id and permission_id == 2:
        raise InputError(description='uid refers to a user who is the only global owner')
    
    for dic in store['users']:
        if dic['auth_user_id'] == u_id:
            # add the uid to channel owner permission list if it is changed to global owner
            if permission_id == 1:
                dic['is_global_owner'] = True
                help.add_uid_to_channel_owner(u_id)            
            # remove the uid from channel owner list if it is changed to global user
            if permission_id == 2:
                dic['is_global_owner'] = False
                help.remove_uid_from_channel_owner(u_id)
    data_store.set(store)
    return {}
    
