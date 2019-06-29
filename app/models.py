from .utils.dao import DataAccessObject
from . import bcrypt


class User:
    @classmethod
    def register(cls, username, password, handle=''):
        if not User.user_exists(username):
            # encrypt password for save
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            DataAccessObject.alter("INSERT INTO users(username, password, handle) VALUES (:username, :password, :handle)", {'username': username, 'password': password, 'handle': handle})
            return True
        else:
            return False

    @classmethod
    def user_exists(cls, username):
        return DataAccessObject.rowcount("SELECT username from users WHERE username = :username", {
            'username': username}) == 1

    @classmethod
    def login(cls, username, password):
        user = DataAccessObject.fetchone("SELECT username, password FROM users WHERE username=:username", {'username': username})
        print(f"USER: {user}")
        if not user:
            return False
        else:
            return bcrypt.check_password_hash(user['password'], password)

    @classmethod
    def change_password(cls, username, password):
        user = DataAccessObject.fetchone('SELECT username FROM users WHERE username = :username',
                                         {'username': username, 'password': password})
        if user:
            password = bcrypt.generate_password_hash(password).decode("utf-8")
            DataAccessObject.alter("UPDATE users SET password = :password WHERE username = :username",
                                   {'username': username, 'password': password})
            return True
        else:
            return False

    @classmethod
    def change_user_data(cls, username, new_username, handle):
        if User.user_exists(username):
            DataAccessObject.alter("UPDATE users SET username = :new_username, handle = :handle WHERE username = :username",
                                   {'username': username, 'new_username': username, 'handle': handle})
            return True
        else:
            return False
