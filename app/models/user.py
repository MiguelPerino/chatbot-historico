from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_, username, password):
        self.id = str(id_)
        self.username = username 
        self.password = password 

    def get_id(self):
        return self.id