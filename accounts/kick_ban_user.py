from django.contrib.sessions.models import Session
from accounts.models import CustomUser

# grab the user in question 
#

def deactivate_user(username:str):
    try:
        # retrieve the user 
        user = CustomUser.objects.get(username=username)
        # delete the user's session(s)
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
        # set the is_active attribute to False
        user.is_active = False
        # save the changes
        user.save()
        return f"user {username} deactivated successfully"
    except CustomUser.DoesNotExist:
        return f"user {username} does not exist"



def delete_user(username:str):
    try:
        # delete the user 
        CustomUser.objects.filter(username=username).delete()
        return f"user {username} deleted successfully"
    except CustomUser.DoesNotExist:
        return f"user {username} does not exist"        