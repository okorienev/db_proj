from . import AbstractAction
from app.models import User, get_session, Role


class CreateUser(AbstractAction):
    ACTION_NAME = "create-user"
    COMMAND_NAME = "creade-user"

    def handle(self) -> None:
        session = get_session()
        while True:
            name = input("Type user name")
            if name:
                break
            print("name can not be empty")
        while True:
            mail = input("Type user email")
            if len(mail) > 10 and '@' in mail:
                break
            print("mail should be longer than 10 digits and contain \'@\'")
        while True:
            login = input("Type user login")
            if len(login) > 6 and login.isalnum():
                break
            print("")
        while True:
            password = input("Type user password")
            if len(password) > 6:
                break
            print("Password should be longer than 6 digits")
        new_usr = User(name=name,
                       login=login,
                       email=mail)
        new_usr.set_password(password)
        roles = session.query(Role).all()
        for index, role in enumerate(roles):
            print("{} - {}".format(index, role.name))
        while True:
            try:
                num = int(input("Type role number"))
                if num < len(roles):
                    new_usr.role = roles[num]
                    break
            except (ValueError, TypeError):
                print("Should be an integer number")
        session.add(new_usr)
        session.commit()

