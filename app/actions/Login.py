from . import AbstractAction
from app.models import get_session, User


class Login(AbstractAction):
    ACTION_NAME = 'login'
    COMMAND_NAME = 'login'

    def __init__(self):
        self._user = None

    @property
    def user(self):
        return self._user if hasattr(self, '_user') else None

    def have_permission(self):
        return True

    def handle(self):
        print("You are now in \'login\' action")
        while True:
            choice = input("Start authentication procedure? (yes/no)").lower()
            if choice in ('yes', 'no'):
                break
        if choice == 'no':
            return
        session = get_session()
        while True:
            login = input('type login: ')
            password = input('type password: ')
            self._user: User = session.query(User).filter(User.login == login).first()
            if self._user and self._user.check_password(password):
                print('Authentication success')
                return
            print("Login credentials are incorrect, please try again")

