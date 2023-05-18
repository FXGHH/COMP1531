from src.help import check_u_id_valid, check_u_id_in_the_channel, searching_user_with_id
from src.help import check_channel_id_valid, check_token_valid, get_user_with_token
from src.help import searching_channel_with_channel_id
import src.help as help
from src.error import AccessError
from src.error import InputError
from src.data_store import data_store


def channel_messages_v2(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50".
    Message with index 0 is the most recent message in the channel.
    This function returns a new index "end" which is the value of "start + 50", or,
    if this function has returned the least recent messages in the channel, returns -1 in "end"
    to indicate there are no more messages to load after this return.

    Arguments:
        token (str) - a session ID used for authorisation
        channel_id (int) - find correspond channel and associated messages
        start(int) - index of channel message

    Exceptions:
        InputError - when Channel ID is not a valid channel
        InputError - when start is greater than the total number of messages in the channel
        AccessError - when Authorised user is not a member of channel with channel_id
        AccessError - when token is invalid

    Return value:
        { messages, start, end }

    '''
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")
    auth_user_id = help.get_auth_user_id(token)
    store = data_store.get()
    channel_list = store['channels']
    message_list = []
    message_dic = {}

    channel_availble = 0
    user_in_channel = 0
    # check the auth_user_id is authorised
    for channel in channel_list:
        if channel_id == channel["channel_id"]:
            channel_availble = 1
            aim_channel = channel
    # check the channel is exit
    if channel_availble == 0:
        raise InputError(description="This channel ID refer a invalid channel")

    channel_user_list = aim_channel["channel_user_id"]
    # User can access the channel
    for channel_user in channel_user_list:
        if channel_user == auth_user_id:
            user_in_channel = 1

    if user_in_channel == 0:
        raise AccessError(description="You're invalid to access this channel")

    # start index large than the total number of messages the total number of messages
    if start > len(aim_channel["message"]):
        raise InputError(
            description="The start meessage index is large than the total number of messages")
    if start < 0:
        raise InputError(description="Message start index can't be negitive")

    elif len(aim_channel["message"]) == start:
        message_dic['messages'] = message_list
        message_dic['start'] = start
        message_dic['end'] = -1
    # channel can return less or equal to 50 messages
    elif len(aim_channel["message"]) - start <= 50:
        start_index = start
        end_index = len(aim_channel["message"])
        while start_index < end_index:
            message_list.append(aim_channel["message"][start_index])
            start_index += 1
        message_dic['messages'] = message_list
        message_dic['start'] = start
        message_dic['end'] = -1

     # len(aim_channel["message"]) - start > 50:
    else:
        start_index = start
        end_index = start + 50
        while start_index < end_index:
            message_list.append(aim_channel["message"][start_index])
            start_index += 1
        message_dic['messages'] = message_list
        message_dic['start'] = start
        message_dic['end'] = end_index

    return message_dic


def channel_invite_v2(token, channel_id, u_id):
    '''
    This function will take in token, channel_id and u_id
    Take someone who is not in the channel to the channel

    Args:
        token (string): the channel member's token
        channel_id (int): the id of the channel
        u_id (int): the id of the invitee

    Exceptions:
        InputError - channel_id does not refer to a valid channel
        InputError - u_id does not refer to a valid user
        InputError - u_id refers to a user who is already a member of the channel
        AccessError - channel_id is valid and the authorised user is not a member of the channel
        AccessError - when token is invalid

    Returns:
        {}
    '''
    # get the data
    store = data_store.get()
    # check for authorised token
    if not check_token_valid(token):
        raise AccessError(
            "Sorry, you have no registed yet"
        )

    # check for channel_id
    if not check_channel_id_valid(channel_id):
        raise InputError(
            "Sorry, the 'channel id' you have entered do not exist"
        )

    # check if the user with input token is a member for the channel
    inviter_id = get_user_with_token(token)
    if not check_u_id_in_the_channel(inviter_id, channel_id):
        raise AccessError(
            "Sorry, you have no right to invite others"
        )

    # check for u_id
    if not check_u_id_valid(u_id):
        raise InputError(
            "Sorry, the user you have invited is not registed yet"
        )

    # check if the user with u_id are not already in the channel
    if check_u_id_in_the_channel(u_id, channel_id):
        raise InputError(
            "Sorry, the user you have invited is already in the channel"
        )

    # adding user to the channel
    new_user = searching_user_with_id(u_id)
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            channel["channel_user_id"].append(u_id)
            data_store.set(store)
            if new_user["is_global_owner"] == True:
                channel["owner_permission"].append(u_id)
                data_store.set(store)

    # notifications
    user_handle = help.get_user_handle(inviter_id)
    ch_name = help.get_channel_name(channel_id)
    notification_detail = f"{user_handle} added you to {ch_name}"
    for user in store["users"]:
        if user["auth_user_id"] == u_id:
            user["notifications"].insert(0,{"dm_id": -1, "channel_id": channel_id, "notification_message": notification_detail})
    data_store.set(store)
    
    help.update_num_channels_joined(u_id,True)
    return {}


def channel_details_v2(token, channel_id):
    '''
    This function will take in token, channel_id 
    Give back the details of the channel

    Args:
        token (string): the channel member's token
        channel_id (int): the id of the channel

    Exceptions:
        InputError - channel_id does not refer to a valid channel
        AccessError - channel_id is valid and the authorised user is not a member of the channel
        AccessError - when token is invalid

    Returns:
        {name,
        is_public,
        owner_members,
        all_members}
    '''
    # get the data
    store = data_store.get()
    # check for authorised token, then get the user id with token
    if not check_token_valid(token):
        raise AccessError(
            "Sorry, you have no registed yet"
        )

    # check for channel_id
    if not check_channel_id_valid(channel_id):
        raise InputError(
            "Sorry, the 'channel id' you have entered do not exist"
        )
    user_id = get_user_with_token(token)
    # check if the user with input token is a member for the channel
    if not check_u_id_in_the_channel(user_id, channel_id):
        raise AccessError(
            "Sorry, you have no right to show the details"
        )

    # gives the dictionary back
    channel_dict = searching_channel_with_channel_id(channel_id)
    return_dict = {}
    return_dict["name"] = channel_dict["channel_name"]
    return_dict["is_public"] = channel_dict["is_public"]
    return_owner_details = []
    return_member_details = []
    owern_id = channel_dict["auth_user_id"]
    member_id = channel_dict["channel_user_id"]
    for owner_check in owern_id:
        for owner in store["users"]:
            if owner_check == owner["auth_user_id"]:
                owner_detail = {}
                owner_detail["u_id"] = owner_check
                owner_detail["email"] = owner["email"]
                owner_detail["name_first"] = owner["name_first"]
                owner_detail["name_last"] = owner["name_last"]
                owner_detail["handle_str"] = owner["handle"]
                return_owner_details.append(owner_detail)
    return_dict["owner_members"] = return_owner_details
    for member_check in member_id:
        for member in store["users"]:
            if member_check == member["auth_user_id"]:
                member_detail = {}
                member_detail["u_id"] = member_check
                member_detail["email"] = member["email"]
                member_detail["name_first"] = member["name_first"]
                member_detail["name_last"] = member["name_last"]
                member_detail["handle_str"] = member["handle"]
                return_member_details.append(member_detail)
    return_dict["all_members"] = return_member_details
    data_store.set(store)
    return return_dict


def channel_join_v2(token, channel_id):
    '''
    This function will take in token, channel_id 
    make the encode auth id join channel

    Args:
        token (string): the user's token
        channel_id (int): the id of the channel

    Exceptions:
        InputError: channel_id does not refer to a valid channel
        InputError: the authorised user is already a member of the channel
        AccessError: channel_id refers to a channel that is private and the authorised user is not already a channel member
                    and is not a global owner
        AccessError: invalid token

    Returns:
        {}
    '''

    store = data_store.get()
    # check token and session
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')

    auth_user_id = help.get_auth_user_id(token)

    # no chid
    ch_id_in = False
    for dic in store['channels']:
        if dic["channel_id"] == channel_id:
            ch_id_in = True
    if ch_id_in == False:
        raise InputError(
            description="Sorry, the 'Channel id' you have enterd do not exist")
    # already in

    au_in_ch = False
    for dic in store['channels']:
        if dic["channel_id"] == channel_id:
            if auth_user_id in dic["channel_user_id"]:
                au_in_ch = True
    if au_in_ch == True:
        raise InputError(
            description="Sorry, the authorised user is already a member of the channel")

    # AccessError is not private, not member, not owner
    is_global_owner = False
    for dic in store['users']:
        if dic["auth_user_id"] == auth_user_id:
            if dic['is_global_owner'] == True:
                is_global_owner = True
    is_private = False
    # is_member = False
    is_onwer = False
    for dic in store['channels']:
        if dic["channel_id"] == channel_id:
            if dic['is_public'] != True:
                is_private = True
            # if auth_user_id in dic["channel_user_id"]:
            #     is_member = True
            if auth_user_id in dic["auth_user_id"]:
                is_onwer = True
    if (is_private == True) and (au_in_ch == False) and (is_onwer == False) and (is_global_owner == False):
        raise AccessError(
            description="Sorry, channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner")

    for dic in store['channels']:
        if dic["channel_id"] == channel_id:
            dic["channel_user_id"].append(auth_user_id)
        if is_global_owner == True:
            dic["owner_permission"].append(auth_user_id)

    data_store.set(store)

    help.update_num_channels_joined(auth_user_id,True)
    return {
    }


def channel_leave_v1(token, channel_id):
    '''
    This function will take in token, channel_id 
    Remove someone who is in the channel 

    Args:
        token (string): the channel member's token
        channel_id (int): the id of the channel

    Exceptions:
        InputError - channel_id does not refer to a valid channel
        AccessError - channel_id is valid and the authorised user is not a member of the channel
        AccessError - when token is invalid

    Returns:
        {}
    '''
    # get data
    store = data_store.get()

    # check token valid
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')

    # decode token to get authorised user id
    auth_user_id = help.get_auth_user_id(token)

    # check channel id valid
    if help.check_channel_id_valid(channel_id) == False:
        raise InputError(
            description="Sorry, the 'Channel id' you have enterd do not exist")

    # check if the uid is in the channel
    if help.check_u_id_in_the_channel(auth_user_id, channel_id) == False:
        raise AccessError(
            description="Sorry, the authorised user is not a member of the channel")

    # get the channel detail
    channel = help.searching_channel_with_channel_id(channel_id)

    # condition: is owner and member
    if help.check_uid_is_owner(auth_user_id, channel['channel_id']) == True and help.check_uid_is_member(auth_user_id, channel['channel_id']) == True:
        channel['auth_user_id'].remove(auth_user_id)
        channel['channel_user_id'].remove(auth_user_id)
        
    # condition: not owner just member
    if help.check_uid_is_owner(auth_user_id, channel['channel_id']) == False and help.check_uid_is_member(auth_user_id, channel['channel_id']) == True:
        channel['channel_user_id'].remove(auth_user_id)

    if help.check_uid_has_owner_permission(auth_user_id, channel['channel_id']) == True:
        channel['owner_permission'].remove(auth_user_id)
    # save the data
    data_store.set(store)

    help.update_num_channels_joined(auth_user_id,False)
    return {}


def channel_addowner_v1(token, channel_id, u_id):
    '''
    This function will take in token, channel_id and u_id
    Set someone to the owner of the channel

    Args:
        token (string): the channel owner's token
        channel_id (int): the id of the channel
        u_id (int): the id of the member to be added to channel owner

    Exceptions:
        InputError - channel_id does not refer to a valid channel
        InputError - u_id does not refer to a valid user
        InputError - u_id refers to a user who is not a member of the channel
        InputError - u_id refers to a user who is already an owner of the channel
        AccessError - channel_id is valid and the authorised user does not have owner permissions in the channel
        AccessError - when token is invalid

    Returns:
        {}
    '''
    # check authorised token valid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    # get authorised user id
    auth_user_id = help.get_auth_user_id(token)

    # check channel id valid
    ch_id_in = help.check_channel_id_valid(channel_id)
    if ch_id_in == True:
        # check authorised user is the channel owner
        au_id_has_owner_permission = help.check_uid_has_owner_permission(auth_user_id, channel_id)
        if au_id_has_owner_permission == False:
            raise AccessError(
                description='Sorry, the authorised user does not have owner permissions in the channel')
    else:
        raise InputError(
            description="Sorry, the 'Channel id' you have enterd do not exist")

    # check if the uid to be added to owner valid
    u_id_valid = help.check_auth_user_id_valid(u_id)
    if u_id_valid == False:
        raise InputError(
            description='Sorry, the uid does not refer to a valid user')

    # check if the uid to be added to owner is in the channel
    au_in_ch = check_u_id_in_the_channel(u_id, channel_id)
    if au_in_ch == False:
        raise InputError(
            description="Sorry, the uid refers to a user who is not a member of the channel")

    # check if the uid to be added to owner is already the channel owner
    u_id_is_owner = help.check_uid_is_owner(u_id, channel_id)
    if u_id_is_owner == True:
        raise InputError(
            description='Sorry, the uid refers to a user who is already an owner of the channel')

    # get data and add the uid to channel owner
    store = data_store.get()
    channel = help.searching_channel_with_channel_id(channel_id)
    channel['auth_user_id'].append(u_id)
    # avoid the global owner already have owner permission
    if u_id not in channel['owner_permission']:
        channel['owner_permission'].append(u_id)
    data_store.set(store)

    help.update_num_channels_joined(u_id,True)
    return {}


def channel_removeowner_v1(token, channel_id, u_id):
    '''
    This function will take in token, channel_id and u_id
    Remove someone from the owner of the channel

    Args:
        token (string): the channel owner's token
        channel_id (int): the id of the channel
        u_id (int): the id of the member to be removed from channel owner

    Exceptions:
        InputError - channel_id does not refer to a valid channel
        InputError - u_id does not refer to a valid user
        InputError - u_id refers to a user who is not a member of the channel
        InputError - u_id refers to a user who is already an owner of the channel
        AccessError - channel_id is valid and the authorised user does not have owner permissions in the channel
        AccessError - when token is invalid

    Returns:
        {}
    '''
    # check the authorised token valid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    # decode the token to get authorised user id
    auth_user_id = help.get_auth_user_id(token)

    # check if the channel id valid
    ch_id_in = help.check_channel_id_valid(channel_id)
    if ch_id_in == True:
        # check if the authorised user has owner permission
        au_id_is_owner = help.check_uid_is_owner(auth_user_id, channel_id)
        if au_id_is_owner == False:
            raise AccessError(
                description='Sorry, the authorised user does not have owner permissions in the channel')
    else:
        raise InputError(
            description="Sorry, the 'Channel id' you have enterd do not exist")

    # check if the uid to be removed from owner valid
    u_id_valid = help.check_auth_user_id_valid(u_id)
    if u_id_valid == False:
        raise InputError(
            description='Sorry, the uid does not refer to a valid user')

    # check if the uid to be removed from owner is in the channel
    au_in_ch = check_u_id_in_the_channel(u_id, channel_id)
    if au_in_ch == False:
        raise InputError(
            description="Sorry, the uid refers to a user who is not a member of the channel")

    # check if the uid to be removed from owner is not a owner of the channel
    u_id_is_owner = help.check_uid_is_owner(u_id, channel_id)
    if u_id_is_owner == False:
        raise InputError(
            description='Sorry, the uid refers to a user who is not an owner of the channel')

    # get channel details
    channel = help.searching_channel_with_channel_id(channel_id)

    # check if the uid to be removed from owner is the only owner of the channel
    if channel['auth_user_id'] == [u_id]:
        raise InputError(
            description='Sorry, the uid refers to a user who is currently the only owner of the channel')

    # get data and remove the uid from the channel owner
    store = data_store.get()
    channel['auth_user_id'].remove(u_id)
    channel['owner_permission'].remove(u_id)
    data_store.set(store)

    help.update_num_channels_joined(u_id,False)
    return {}
