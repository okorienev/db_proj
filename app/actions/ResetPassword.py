from . import AbstractAction
from app.models import User, get_session


class ResetPassword(AbstractAction):

    ACTION_NAME = 'reset-pass'
    COMMAND_NAME = 'reset-pass'

    def handle(self):
        session = get_session()
        print("You are now in \'reset-pass\' action")

        while True:
            email = input("Enter your email: ")
            self._user: User = session.query(User).filter(User.email == email).first()
            if self._user:
                while True:
                    pass1 = input("Enter your new password: ")
                    pass2 = input("Repeat your new password: ")
                    if pass1 == pass2:
                        self._user.set_password(pass1)
                        while True:
                            choice = input("Are you sure you want to reset your old password? (yes/no)").lower()
                            if choice in ('yes', 'no'):
                                break
                        if choice == 'no':
                            print("Good luck!")
                            session.close()
                            return
                        print("Your password was changed successfully!")
                        session.commit()
                        session.close()
                        return
                    print("Your password does not mach!")
            print("Can not find this email! Try one more time)")


