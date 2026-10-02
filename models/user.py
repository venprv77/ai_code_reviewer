from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_id, fullname, username, email, role):

        self.id = user_id
        self.fullname = fullname
        self.username = username
        self.email = email
        self.role = role