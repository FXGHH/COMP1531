from socket import herror
from src.data_store import data_store
from src.error import AccessError
import src.help as help
 
def user_stats_v1(token):
    '''
    Fetches the required statistics about this user's use of UNSW Seams.

    Args:
        token (string): the channel owner's token

    Exception:
        AccessError - when token is invalid

    Returns:
        { user_stats }
    '''
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    user_id = help.get_auth_user_id(token)
    current_user = help.get_user_with_auth_user_id(user_id)
 
    user_stats = {}
    user_stats['channels_joined'] = current_user['user_stats']['channels_joined']
    user_stats['dms_joined'] = current_user['user_stats']['dms_joined']
    user_stats['messages_sent'] = current_user['user_stats']['messages_sent']
    
    num_channels_joined = user_stats['channels_joined'][-1]['num_channels_joined']
    print( (user_stats['channels_joined']))
    num_dms_joined = user_stats['dms_joined'][-1]['num_dms_joined']
    num_messages_sent = user_stats['messages_sent'][-1]['num_messages_sent']
    total_self = num_channels_joined + num_dms_joined + num_messages_sent
    print(num_channels_joined , num_dms_joined , num_messages_sent)
    total = help.get_sum_for_user_stats()
    
    user_stats['involvement_rate'] = 0 if total == 0 else total_self/total
 
    return {'user_stats':user_stats }

def users_stats_v1(token):
    '''
    Fetches the required statistics about the use of UNSW Seams.

    Args:
        token (string): the channel owner's token

    Exception:
        AccessError - when token is invalid

    Returns:
        { workspace_stats  }
    '''
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token")

    store = data_store.get()
    current_stats = store['workspace_stats']
 
    workspace_stats = {}
    workspace_stats['channels_exist'] = current_stats['channels_exist']
    workspace_stats['dms_exist'] = current_stats['dms_exist']
    workspace_stats['messages_exist'] = current_stats['messages_exist']

    num_users_who_have_joined_at_least_one_channel_or_dm = help.get_user_num_for_users_stats()
    num_users = len(store['users'])
    workspace_stats['utilization_rate'] = 0 if num_users == 0 else num_users_who_have_joined_at_least_one_channel_or_dm/num_users

    return  {'workspace_stats':workspace_stats }
 