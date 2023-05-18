from src.error import InputError, AccessError
from src.data_store import data_store
import src.help as help


def dm_create_v1(token, u_ids):
    '''
    This function will take in token,  u_ids
    decode token get user id and use this id to
    invite and create others.
    u_ids contains the user(s) that this DM is directed to,
    and will not include the creator.
    The creator is the owner of the DM. 
    name should be automatically generated based on the users that are in this DM. 
    The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, 
    e.g. 'ahandle1, bhandle2, chandle3'.

    Args:
        token (string): the channel member's token
        u_ids list(int): the id of the u_ids

    Exceptions:
        InputError: any u_id in u_ids does not refer to a valid user
        InputError: there are duplicate 'u_id's in u_ids
        InputError: dm creator in u_ids
        AccessError: invalid token
    Returns:
        { dm_id }
    '''
    store = data_store.get()

    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    auth_user_id = help.get_auth_user_id(token)

    return_result = {}
    if u_ids == []:

        handle = ''
        for user in store["users"]:
            if user["auth_user_id"] == auth_user_id:
                handle = user["handle"]

        dm_creator_id = [auth_user_id]
        dm_members_id = [auth_user_id]
        dm_messages = []
        dm_id = store['total_dm'] + 1
        store['total_dm'] += 1
        dm_name = handle

        new_dm = {}
        new_dm["dm_id"] = dm_id
        new_dm["dm_creator_id"] = dm_creator_id
        new_dm["dm_members_id"] = dm_members_id
        new_dm["dm_messages"] = dm_messages
        new_dm["dm_name"] = dm_name
        store["dm"].append(new_dm)
        return_result["dm_id"] = dm_id
        data_store.set(store)

    if u_ids != []:
        if auth_user_id in u_ids:
            raise InputError(description='Sorry,creater should not in u_ids')
        for uesr in u_ids:
            if help.check_auth_user_id_valid(uesr) == False:
                raise InputError(
                    description='Sorry, u_id in u_ids does not refer to a valid user')

        # check duplicate
        check_u_ids = []
        for id in u_ids:
            if id not in check_u_ids:
                check_u_ids.append(id)

        if len(check_u_ids) != len(u_ids):
            raise InputError(
                description='Sorry, there are duplicate u_ids in u_ids')

        handle = ''
        for user in store["users"]:
            if user["auth_user_id"] == auth_user_id:
                handle = user["handle"]

        dm_name_list = [handle]
        for id in u_ids:
            for user in store["users"]:
                if id == user["auth_user_id"]:
                    dm_name_list.append(user["handle"])
        dm_name_list.sort()

        comma = ", "
        dm_name = comma.join(dm_name_list)

        # dm_id = len(store["dm"]) + 1
        dm_id = store['total_dm'] + 1
        store['total_dm'] += 1
        dm_creator_id = [auth_user_id]
        dm_members_id = []
        dm_members_id.append(auth_user_id)
        for id in u_ids:
            dm_members_id.append(id)
        dm_messages = []

        new_dm = {}
        new_dm["dm_id"] = dm_id
        new_dm["dm_creator_id"] = dm_creator_id
        new_dm["dm_members_id"] = dm_members_id
        new_dm["dm_messages"] = dm_messages
        new_dm["dm_name"] = dm_name
        store["dm"].append(new_dm)

        # notifications
        for uid in u_ids:
            user_handle = help.get_user_handle(auth_user_id)
            dm_name = help.get_dm_name(dm_id)
            notification_detail = f"{user_handle} added you to {dm_name}"
            for user in store["users"]:
                if user["auth_user_id"] == uid:
                    user["notifications"].insert(0,{"dm_id": dm_id, "channel_id": -1, "notification_message": notification_detail})

        data_store.set(store)

        return_result["dm_id"] = dm_id
    help.update_num_dms_joined(auth_user_id,True)

    for id in u_ids:
        help.update_num_dms_joined(id,True)

    help.update_dms_exist(True)

    #print(store)
    return return_result


def dm_list_v1(token):
    '''
    This function will take in token
    decode token get user id and use this auid to
    returns the list of DMs that the user is a member of.

    Args:
        token (string): the channel member's token

    Exceptions:
        AccessError: invalid token

    Returns:
        { dms }
    '''
    store = data_store.get()
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    auth_user_id = help.get_auth_user_id(token)

    dms = []

    for user in store["dm"]:
        if auth_user_id in user["dm_members_id"]:
            dms.append({"dm_id": user["dm_id"], "name": user["dm_name"]})

    return {"dms": dms}


def dm_remove_v1(token, dm_id):
    '''
    This function will take in token
    decode token get user id and use this auid to
    remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Args:
        token (string): the channel member's token
        dm_id (int): the id of dm

    Exceptions:
        AccessError: invalid token
        InputError: dm_id does not refer to a valid DM
        AccessError: dm_id is valid and the authorised user is not the original DM creator
        AccessError: dm_id is valid and the authorised user is no longer in the DM
    Returns:
        {}
    '''
    store = data_store.get()
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')

    auth_user_id = help.get_auth_user_id(token)

    if help.dm_id_is_valid(dm_id) == False:
        raise InputError(
            description='Sorry, dm_id does not refer to a valid DM')

    is_dm_creator = False
    for id in store["dm"]:
        if auth_user_id in id["dm_creator_id"]:
            is_dm_creator = True

    if help.uid_in_dm(auth_user_id) == False and help.dm_id_is_valid(dm_id) == True:
        raise AccessError(
            description="Sorry, dm_id is valid and the authorised user is no longer in the DM")

    if is_dm_creator == False and help.dm_id_is_valid(dm_id) == True:
        raise AccessError(
            description="Sorry, dm_id is valid and the authorised user is not the original DM creator")

    user_list = []
    for single_dm in store['dm']:
        if single_dm["dm_id"] == dm_id:
            user_list.extend(single_dm['dm_creator_id'])
            user_list.extend(single_dm['dm_members_id'])
            store['dm'].remove(single_dm)
    data_store.set(store)
    
    for user_id in set(user_list):
        help.update_num_dms_joined(user_id,False)

    help.update_dms_exist(False)

    return {}


def dm_details_v1(token, dm_id):
    """
    Given a DM with ID dm_id that the authorised user is a member of,
    provide basic details about the DM.

    Args:
        token (string): the channel member's token
        dm_id (int): the id of the dm

    Exceptions:
        AccessError: invalid token
        InputError: dm_id does not refer to a valid DM
        AccessError: dm_id is valid and the authorised user is not a member of the DM

    Returns:
        {name, members}
    """
    store = data_store.get()
    if not help.check_token_valid(token):
        raise AccessError(
            description="Sorry, you have no registed yet"
        )

    # check for channel_id
    if not help.check_dm_id_valid(dm_id):
        raise InputError(
            description="Sorry, the 'dm_id' you have entered do not exist"
        )

    user_id = help.get_user_with_token(token)
    # check if the user with input token is a member for the channel
    if not help.check_u_id_in_the_dm(user_id):
        raise AccessError(
            description="Sorry, you have no right to show the details"
        )

    return_dict = {}
    dm_dict = help.searching_dm_with_dm_id(dm_id)
    return_dict["name"] = dm_dict["dm_name"]
    return_member_details = []
    member_id = dm_dict["dm_members_id"]
    for mem in member_id:
        for user in store["users"]:
            if mem == user["auth_user_id"]:
                r_mem = help.get_user_details(mem)
                return_member_details.append(r_mem)
    return_dict["members"] = return_member_details
    return return_dict


def dm_leave_v1(token, dm_id):
    """
    Given a DM ID, the user is removed as a member of this DM.
    The creator is allowed to leave and the DM will still exist if this happens. 
    This does not update the name of the DM.

    Args:
        token (string): the channel member's token
        dm_id (int): the id of the dm

    Exceptions:
        AccessError: invalid token
        InputError: dm_id does not refer to a valid DM
        AccessError: dm_id is valid and the authorised user is not a member of the DM

    Returns:
        {}
    """
    store = data_store.get()
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    auth_user_id = help.get_auth_user_id(token)

    if help.dm_id_is_valid(dm_id) == False:
        raise InputError(
            description='Sorry, dm_id does not refer to a valid DM')

    if help.uid_in_dm(auth_user_id) == False and help.dm_id_is_valid(dm_id) == True:
        raise AccessError(
            description="Sorry, dm_id is valid and the authorised user is no longer in the DM")

    for dm_member in store["dm"]:
        if dm_member["dm_id"] == dm_id:
            dm_member["dm_members_id"].remove(auth_user_id)
            if auth_user_id in dm_member["dm_creator_id"]:
                dm_member["dm_creator_id"].remove(auth_user_id)
    data_store.set(store)

    help.update_num_dms_joined(auth_user_id,False)
    return {}


def dm_messages_v1(token, dm_id, start):
    '''
    Given a DM with ID dm_id that the authorised user is part of, return up to 50 messages
    between index "start" and "start + 50". Message with index 0 is the most recent message 
    in the channel. This function returns a new index "end" which is the value of "start + 50",
    or, if this function has returned the least recent messages in the channel, returns -1 in "end" to
    indicate there are no more messages to load after this return.

    Arguments:
        token(str) - token of the dm creator
        dm_id (int) - the dm ID
        start (int) - index of the dm message

    Exceptions:
        InputError - dm id is invalid
        InputError - when start is greater than the total number of messages in the DM
        AccessError - authorised user is not a member of dm(not in dm member list)
        AccessError - token is invalid

    Return Value:
        Returns {messages, start, end}
    '''
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    u_id = help.get_auth_user_id(token)

    message_list = []
    # invalid token

    if help.check_dm_id_valid(dm_id) == False:
        raise InputError(description="Invalid DM id !!!")
    dm_dic = help.searching_dm_with_dm_id(dm_id)
    # u_id not mumber of DM
    if u_id not in dm_dic['dm_members_id'] and u_id not in dm_dic['dm_creator_id']:
        raise AccessError(
            description="You are not a member of this DM")

    # start index wrong

    if start > len(dm_dic['dm_messages']):
        raise InputError(
            description="The start meessage index is large than the total number of messages")
    if start < 0:
        raise InputError(
            description="Message start index can't be negitive")
    message_end_index = start + 50
    if message_end_index >= len(dm_dic['dm_messages']):
        end = -1
    else:
        end = message_end_index

    if len(dm_dic['dm_messages']) - start <= 50:
        message_end_index = len(dm_dic['dm_messages'])
    # collect the correspond messages
    if start == len(dm_dic['dm_messages']):
        return {'messages': message_list,
                'start': start,
                'end': end}
    else:
        for i in range(start, message_end_index):
            message_list.append(dm_dic['dm_messages'][i])

    return {'messages': message_list,
            'start': start,
            'end': end}
