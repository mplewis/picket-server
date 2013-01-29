import yaml
import site_config

from flask.ext.login import UserMixin

class User(UserMixin):
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password = password
        self.active = is_active
    def __repr__(self):
        return 'User "' + self.username + '"'
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.username)
    def check_password(self, input):
        if self.password == input:
            return True
        else:
            return False

def load_users_from_file():
    with open(site_config.USER_LIST_FILE) as userFile:
        userData = yaml.load(userFile)
        users = {}
        for user in userData['users']:
            username = user['username']
            password = user['password']
            is_active = user['active']
            user_obj = User(username, password, is_active=is_active)
            users[username] = user_obj
        return users

def get_user(user_id, user_dict):
    if user_id in user_dict:
        return user_dict[user_id]
    else:
        return None

if __name__ == '__main__':
    all_users = load_users_from_file()
    print load_users_from_file()
    print get_user('matt')
    print get_user('not_a_user')