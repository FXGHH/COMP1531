from src.data_store import data_store
import src.help as help
from src.channels import channels_list_v2
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_list_v1
def clear_v1():
    '''
    Resets the internal data of the application to its initial state

    Args:
        {}

    Exceptions:

    Returns:
        {}
    '''
 
    data_store.reset()
 
 
    return {}

def search_v1(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels/DMs 
    that the user has joined that contain the query (case-insensitive). 
    There is no expected order for these messages.

    Args:
        token : the user's token.
        query_str: query(case-insensitive).

    Exception:
        AccessError: when token is invalid
        InputError: length of query_str is less than 1 or over 1000 characters

    Returns:
        {messages}
    '''
    store = data_store.get()
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    auth_user_id = help.get_auth_user_id(token)

    if len(query_str) > 1000 or len(query_str) < 1:
        raise InputError(description="length of query_str is less than 1 or over 1000 characters")

    # channels part
    # get all channel id user in
    channel_id_list = []
    channel_user_in = channels_list_v2(token)["channels"]
    for ch in channel_user_in:
        channel_id_list.append(ch["channel_id"])

    # get channels all message
    all_ch_message = []
    for chid in channel_id_list:
        for dic in store["channels"]:
            if int(chid) == int(dic["channel_id"]):
                all_ch_message.append(dic["message"])

    user_ch_result = []

    # get all channels message result
    for auid in all_ch_message:
        for list in auid:
            if list['u_id'] == auth_user_id and list["message"].find(query_str) != -1:
                return_dic = {}
                return_dic["message_id"] = list["message_id"]
                return_dic["u_id"]  = list["u_id"]
                return_dic["message"] = list["message"]
                return_dic["time_sent"] = list["time_created"]
                return_dic["reacts"] = list["reacts"]
                return_dic["is_pinned"] = list["is_pinned"]
                user_ch_result.append(return_dic)

    # dms part
    dm_id_list = []
    dm_user_in = dm_list_v1(token)["dms"]
    for dm in dm_user_in:
        dm_id_list.append(int(dm['dm_id']))

    #get dms all messages
    all_dm_message = []
    for dmid in dm_id_list:
        for dic in store["dm"]:
            if int(dmid) == int(dic['dm_id']):
                all_dm_message.append(dic["dm_messages"])

    user_dm_result = []
    for auid in all_dm_message:
        for list in auid:
            if list['u_id'] == auth_user_id and list["message"].find(query_str) != -1:
                return_dic = {}
                return_dic["message_id"] = list["message_id"]
                return_dic["u_id"]  = list["u_id"]
                return_dic["message"] = list["message"]
                return_dic["time_sent"] = list["time_created"]
                return_dic["reacts"] = list["reacts"]
                return_dic["is_pinned"] = list["is_pinned"]
                user_dm_result.append(return_dic)

    dm_and_ch_result = user_ch_result + user_dm_result
    return {"messages": dm_and_ch_result}

def notifications_get_v1(token):
    '''

    Return the user's most recent 20 notifications,
    ordered from most recent to least recent.

    Args:
        token: the user's token.

    Exception:
        AccessError: token is invalid

    Returns:
        {notifications}
    '''

    store = data_store.get()
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')
    auth_user_id = help.get_auth_user_id(token)

    for user in store["users"]:
        if user["auth_user_id"] == auth_user_id:
            notifications = user["notifications"][0:20]
    data_store.set(store)

    return {"notifications": notifications}
