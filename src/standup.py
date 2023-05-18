import time
import threading
from src.error import InputError, AccessError
from src.data_store import data_store
import src.help as help
from src.message import message_send_v1

def standup_start_v1(token, channel_id, length):
    '''
    This function will take in token, channel_id, length
    For a given channel, start the standup period whereby for the next "length" seconds if someone calls "standup/send" with a message, 
    it is buffered during the X second window then at the end of the X second window a message will be added to the message queue in the channel from the user who started the standup. 
    "length" is an integer that denotes the number of seconds that the standup occurs for. If no standup messages were sent during the duration of the standup, no message should be sent at the end.

    Args:
        token (string): authorised user token
        channel_id (int): target channel
        length : standup time
    
    Exception:
    InputError when any of:    
        channel_id does not refer to a valid channel
        length is a negative integer
        an active standup is currently running in the channel
      
    AccessError when:     
        authorised token is invalid 
        channel_id is valid and the authorised user is not a member of the channel
        
    Returns:
        { 'time_finish': time_finish}
    '''
    # check token valid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")
    
    # get u_id from token
    auth_user_id = help.get_auth_user_id(token)
    
    # check channel id valid
    ch_id_in = help.check_channel_id_valid(channel_id)
    if ch_id_in == True:
        # check authorised user is channel member
        au_id_is_member = help.check_uid_is_member(auth_user_id, channel_id)
        if au_id_is_member == False:
            raise AccessError(
                description='Sorry, the authorised is not a member of the channel')
        
        # check if a standup is already actived
        if help.check_standup_active(channel_id) == True:
            raise InputError(
            description='Sorry, standup already active'
        )
    else:
        raise InputError(
            description="Sorry, the 'channel id' you have enterd do not exist")
    # check length is greater than 0
    if length < 0:
        raise InputError(
            description='Sorry, length should not be a negative integer'
        )
    # get data
    store = data_store.get()
    # define finish time for standup
    time_finish = int(time.time()) + length
    
    # append standup details to datastore
    new_dic = {}
    standup_messages = []
    new_dic['channel_id'] = channel_id
    new_dic['time_finish'] = time_finish
    new_dic['standup_messages'] = standup_messages
    store["standups"].append(new_dic)

    # when time finish do standup_send_summary
    t = threading.Timer(length, standup_send_summary, args = [token, channel_id])
    t.daemon = True
    t.start()
    
    data_store.set(store)
    
    return {
        'time_finish': time_finish
    }

def standup_active_v1(token, channel_id):
    '''
    This function will take in token, channel_id
    For a given channel, return whether a standup is active in it, and what time the standup finishes.
    If no standup is active, then time_finish returns None.

    Args:
        token (string): authorised user token
        channel_id (int): target channel
    
    Exception:
    InputError when: 
        channel_id does not refer to a valid channel
      
      AccessError when:
        authorised token invalid
        channel_id is valid and the authorised user is not a member of the channel
        
    Returns:
        { "is_active": is_active,
        "time_finish": time_finish}
    '''
    # check token valid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")
    
    # get u_id from authorised token
    auth_user_id = help.get_auth_user_id(token)
    
    # check channel id valid    
    ch_id_in = help.check_channel_id_valid(channel_id)
    if ch_id_in == True:
        # check authorised user is channel member
        au_id_is_member = help.check_uid_is_member(auth_user_id, channel_id)
        if au_id_is_member == False:
            raise AccessError(
                description='Sorry, the authorised is not a member of the channel')
    else:
        raise InputError(
            description="Sorry, the 'channel id' you have enterd do not exist")
    
    is_active = False
    time_finish = None

    store = data_store.get()
    # check if the standup in target channel is actived
    for dic in store["standups"]:
        if dic["channel_id"] == channel_id:
            is_active = True
            time_finish = dic["time_finish"]
    
    data_store.set(store)
    
    return {
        "is_active": is_active,
        "time_finish": time_finish
    }

def standup_send_v1(token, channel_id, message):
    '''
    This function will take in token, channel_id
    Sending a message to get buffered in the standup queue, 
    assuming a standup is currently active. Note: @ tags should not be parsed as proper tags when sending to standup/send

    Args:
        token (string): authorised user token
        channel_id (int): target channel
        message (string): message to send
    
    Exception:
    InputError when any of:
        channel_id does not refer to a valid channel
        length of message is over 1000 characters
        an active standup is not currently running in the channel
      
      AccessError when:
        authorised token invalid  
        channel_id is valid and the authorised user is not a member of the channel
        
    Returns:
        {}
    '''
    # check token valid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    # get u_id from token
    auth_user_id = help.get_auth_user_id(token)
    
    # check channel id valid
    ch_id_in = help.check_channel_id_valid(channel_id)
    if ch_id_in == True:
        # check authorised user is channel member
        au_id_is_member = help.check_uid_is_member(auth_user_id, channel_id)
        if au_id_is_member == False:
            raise AccessError(
                description='Sorry, the authorised is not a member of the channel')
        # check if standup is already actived
        if help.check_standup_active(channel_id) == False:
            raise InputError(
                description='Sorry, an active standup is not currently running in the channel'
        )      
    else:
        raise InputError(
            description="Sorry, the 'channel id' you have enterd do not exist")
    
    # check message length is valid
    if len(message) > 1000:
        raise InputError(description="Sorry, message must be less than 1000 characters")
    
    # get user with u_id
    user = help.searching_user_with_id(auth_user_id)
    
    # defien the style of message sent
    message_append = user['handle'] + ': ' + message

    # get data from datastore
    store = data_store.get()
    # find the channel and add the message to standup_message list
    for dic in store['standups']:
        if dic['channel_id'] == channel_id:
            dic['standup_messages'].append(message_append)
    
    data_store.set(store)
    
    return {}

def standup_send_summary(token, channel_id):
    '''
    This function will take in token, channel_id
    Summary total messsages in the standup time and transpose into one string and add it to the channel

    Args:
        token (string): authorised user token
        channel_id (int): target channel
    
    Returns:
        {}
    '''
    # get data from datastore
    store = data_store.get()
    # find the target channel_id and store the standup_message into a list called message_list
    message_list = []
    for dic in store['standups']:
        if dic['channel_id'] == channel_id:
            message_list = dic['standup_messages']
    # transpose the message to string
    standup_send_summary = ''
    for message in message_list:
        standup_send_summary += message + '\n'
    
    # delete the last space
    standup_send_summary = standup_send_summary.rstrip('\n')
    
    # send the total message if is not NULL
    if standup_send_summary != '':
        message_send_v1(token, channel_id, standup_send_summary)
    # when standup finish removed the standup in datastore
    for dic in store['standups']:
        if dic['channel_id'] == channel_id:
            store['standups'].remove(dic)
    
    data_store.set(store)
    return