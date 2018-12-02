from app.actions import AbstractAction
from app.models import get_session, Role, Right, OperationType


class CreateRole(AbstractAction):

    ACTION_NAME = 'create-role'
    COMMAND_NAME = 'create-role'

    def handle(self) -> None:
        if not self.start_procedure():
            return
        role = Role()
        session = get_session()
        role.name = self.read_role_name(session.query(Role).all())

        operations = session.query(OperationType).all()
        self.print_available_operations(operations)
        operations_numbers = self.read_role_operations(len(operations))

        for operation_num in set(operations_numbers):
            right = session.query(Right).filter(Right.operation_type == operations[int(operation_num)]).first()
            role.rights.append(right)

        self.end_procedure(role)
        session.add(role)
        session.commit()

    @staticmethod
    def start_procedure():
        print("You are now in 'create role' action.")
        while True:
            choice = input("Start creating role procedure? (y/n)").lower()
            if choice in ('y', 'n'):
                break
        if choice == 'y':
            return True

    @staticmethod
    def read_role_name(roles):
        while True:
            role_name = input("Enter role name:")
            for r in roles:
                if role_name == r.name:
                    print("Role '{}' already exists!".format(role_name))
                    break
            else:
                return role_name

    @staticmethod
    def print_available_operations(operations):
        print("Available rights:")
        for index, operation in enumerate(operations):
            print("{} {}".format(index, operation.name))

    @staticmethod
    def check_operations_numbers(operations_numbers, operations_len):
        for operation_number in set(operations_numbers):
            try:
                num = int(operation_number)
            except ValueError:
                return False
            if not 0 <= num < operations_len:
                return False
        return True

    @staticmethod
    def read_role_operations(operations_len):
        while True:
            operations_numbers = input("Enter rights numbers separated by space:").split(' ')
            if CreateRole.check_operations_numbers(operations_numbers, operations_len):
                break
            else:
                print("Incorrect rights numbers!")
        return operations_numbers

    @staticmethod
    def end_procedure(role):
        print("Role '{}' was successfully created and have rights to:".format(role.name))
        for right in role.rights:
            print("\t- {}".format(right.operation_type.name))
