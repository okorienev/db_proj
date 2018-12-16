from abc import abstractmethod
from app.models import get_session, User, OperationType, Operation
import datetime


class AbstractAction:
    """
    class to declare common interface for console implementation of use cases
    """
    ACTION_NAME: str = None
    COMMAND_NAME: str = None

    def log_operation(self):
        session = get_session()
        operation = Operation(date=datetime.datetime.utcnow(),
                              user=self.user,
                              operation_type=session.query(OperationType).filter(
                                  OperationType.name == self.ACTION_NAME).first())
        session.add(operation)
        session.commit()
        del session

    def __init__(self, user: User):
        self.user: User = user

    def have_permission(self) -> bool:
        """
        todo universal permission check for all cases
        :return: should return boolean value of current user permission to commit action
        """
        return self.ACTION_NAME in [right.operation_type.name for right in self.user.role.rights]

    @abstractmethod
    def handle(self) -> None:
        """
        method which gets control over the application (input, output, queries, etc)
        :return:
        """
        raise NotImplementedError
