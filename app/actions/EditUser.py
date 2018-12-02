from app.actions import AbstractAction
from app.models import get_session, User, Role


class EditUser(AbstractAction):

    ACTION_NAME = 'edit-user'
    COMMAND_NAME = 'edit-user'

    FIELDS = ("name", "login", "email", "password", "role")

    def handle(self) -> None:
        if not self.start_procedure():
            return
        session = get_session()

        users = session.query(User).all()
        self.print_users(users)
        user = self.read_user(users)

        self.print_possible_fields()
        changes = self.edit_fields(user, session.query(Role).all())

        session.add(user)
        session.commit()
        self.end_process(user.name, changes)

    @staticmethod
    def start_procedure():
        print("You are now in 'edit user' action.")
        while True:
            choice = input("Start editing user procedure? (y/n)").lower()
            if choice in ('y', 'n'):
                break
        if choice == 'y':
            return True

    @staticmethod
    def print_users(users):
        print("Existing users:")
        for index, user in enumerate(users):
            print("{} {}".format(index, user.name))

    @staticmethod
    def read_user(users):
        while True:
            try:
                user_num = int(input("Enter user number:"))
            except ValueError:
                print("Incorrect user number!")
                continue
            if 0 <= user_num < len(users):
                return users[user_num]
            else:
                print("Incorrect user number!")

    @staticmethod
    def print_possible_fields():
        print("Existing fields:")
        for index, field in enumerate(EditUser.FIELDS):
            print("{} {}".format(index, field))

    @staticmethod
    def read_field():
        while True:
            try:
                field_num = int(input("Enter field number:"))
            except ValueError:
                print("Incorrect field number!")
                continue
            if 0 <= field_num < len(EditUser.FIELDS):
                return EditUser.FIELDS[field_num]
            else:
                print("Incorrect field number!")

    @staticmethod
    def print_roles(roles):
        print("Existing roles:")
        for index, role in enumerate(roles):
            print("{} {}".format(index, role.name))

    @staticmethod
    def read_role(roles):
        while True:
            try:
                role_num = int(input("Enter role number:"))
            except TypeError:
                print("Incorrect role number!")
                continue
            if 0 <= role_num < len(roles):
                return roles[role_num]
            else:
                print("Incorrect role number!")

    @staticmethod
    def edit_field(field, user, roles):
        if field == "role":
            EditUser.print_roles(roles)
            role = EditUser.read_role(roles)
            role.users.append(user)
            return role.name

        value = input("Enter value:")
        if field == "name":
            user.name = value
        elif field == "login":
            user.login = value
        elif field == "email":
            user.email = value
        elif field == "password":
            user.set_password(value)
        return value

    @staticmethod
    def edit_fields(user, roles):
        changes = {}
        while True:
            choice = input("Edit '{}' user field? (y/n)".format(user.name)).lower()
            if choice == 'n':
                break
            if choice == 'y':
                field = EditUser.read_field()
                value = EditUser.edit_field(field, user, roles)
                changes[field] = value
        return changes

    @staticmethod
    def end_process(user_name, changes):
        if len(changes) == 0:
            return
        print("User '{}' was successfully edited.".format(user_name))
        print("Changed:")
        for field, value in changes.items():
            print("field '{}' to '{}'".format(field, value))
