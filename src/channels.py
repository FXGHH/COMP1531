from src.error import InputError, AccessError
from src.data_store import data_store
import src.help as help


def channels_list_v2(token):
    '''
    This function will take in token
    List channels which the authorised user is in

    Args:
        token (string): the user's token

    Exception:
        AccessError - when token is invalid

    Returns:
        {'channels': [{'channel_id': xxx, 'name': xxx}, {'channel_id': xxx, 'name': xxx}, ...]}
    '''
    # check authorised token valid
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')

    # get authorised user id
    auth_user_id = help.get_auth_user_id(token)

    # generate a structure to store the data we want
    new_list = []
    new_dic = {}
    store = data_store.get()
    for dic in store["channels"]:
        personal_channel = {}
        if auth_user_id in dic["auth_user_id"] or auth_user_id in dic["channel_user_id"]:
            personal_channel["channel_id"] = dic["channel_id"]
            personal_channel["name"] = dic["channel_name"]
            new_list.append(personal_channel)
    new_dic["channels"] = new_list
    return new_dic


def channels_create_v2(token, name, is_public):
    '''
    This function will take in token, name, is_public
    Create a new channel with the authorised token

    Args:
        token (string): the user's token
        name (string): new channel name
        is_public (bool): the new channel is public or private

    Exception:
        InputEroor - length of name is less than 1 or more than 20 characters
        AccessError - when token is invalid

    Returns:
        {'channel_id': new channel id}
    '''
    # check authorised token valid
    if help.check_token(token) == False:
        raise AccessError(description='Sorry, invalid token')

    # get data and decode the token to get authorised user id
    store = data_store.get()
    auth_user_id = help.get_auth_user_id(token)

    # check if the setted name is valid
    if len(name) < 1 or len(name) > 20:
        raise InputError(
            description="Length of name should not be less than 1 or more than 20 characters")

    # generate new channel id and save data
    new_channel_id = len(store['channels']) + 1
    new_dic = {}
    auth_user_ids = []
    auth_user_ids.append(auth_user_id)
    auth_user_id1 = []
    auth_user_id1.append(auth_user_id)
    message = []
    owner_permission = []
    owner_permission.append(auth_user_id)
    new_dic["channel_id"] = new_channel_id
    new_dic["auth_user_id"] = auth_user_id1
    new_dic["channel_name"] = name
    new_dic["is_public"] = is_public
    new_dic["channel_user_id"] = auth_user_ids
    new_dic["message"] = message
    new_dic["channel_creator"] = auth_user_id
    new_dic["owner_permission"] = owner_permission
    store["channels"].append(new_dic)
    data_store.set(store)

    help.update_channels_exist()
    help.update_num_channels_joined(auth_user_id,True)
    
    return {
        "channel_id": new_channel_id,
    }


def channels_listall_v2(token):
    """
    Provides a list of all channels (and their associated details).

    Arguments:
    token (str) - a session ID used for authorisation

    Exceptions:
    AccessError- when token or session id are invalid

    Return Value:
    A dictionary which contains a list of every channel.
    Each channel dictionary contains the name of the channel and channel ID.
    """

    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    auth_user_id = help.get_auth_user_id(token)
    store = data_store.get()
    channel_list_all = store
    user_list = store
    ret_list_channel = []
    new_dic = {}
    for user in user_list['users']:
        if user['auth_user_id'] == auth_user_id:
            for channel in channel_list_all['channels']:
                channel_list_dic = {}
                channel_list_dic["channel_id"] = channel["channel_id"]
                channel_list_dic["name"] = channel["channel_name"]
                ret_list_channel.append(channel_list_dic)
    new_dic["channels"] = ret_list_channel
    return new_dic
