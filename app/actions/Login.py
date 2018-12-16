from . import AbstractAction
from app.models import get_session, User
from .ResetPassword import ResetPassword


class Login(AbstractAction):
    ACTION_NAME = 'login'
    COMMAND_NAME = 'login'

    def __init__(self):
        super().__init__(None)

    def have_permission(self):
        return True

    def handle(self):
        print("You are now in \'login\' action")
        # while True:
        #     choice = input("Start authentication procedure? (yes/no)").lower()
        #     if choice in ('yes', 'no'):
        #         break
        # if choice == 'no':
        #     return
        session = get_session()
        while True:
            login = input('type login: ')
            password = input('type password: ')
            self.user: User = session.query(User).filter(User.login == login).first()
            if self.user and self.user.check_password(password):
                print('Authentication success')
                return
            print("Login credentials are incorrect, please try again")
            while True:
                choice = input("Restore password? (yes/no)").lower()
                if choice in ('yes', 'no'):
                    break
            if choice == "yes":
                restore = ResetPassword(User())
                restore.handle()
