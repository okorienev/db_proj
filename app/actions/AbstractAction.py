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
                              operation_type=self.operation_type)
        session.add(operation)
        session.commit()
        del session

    def __init__(self, user: User):
        self.user: User = user
        session = get_session()
        self.operation_type: OperationType = session.query(OperationType).filter(
            OperationType.name==self.ACTION_NAME
        ).first()
        del session
        if not self.operation_type:
            raise ValueError("Can't find operation with given type")

    def have_permission(self) -> bool:
        """
        todo universal permission check for all cases
        :return: should return boolean value of current user permission to commit action
        """
        return self.user.role in self.operation_type.rights.roles

    @abstractmethod
    def handle(self) -> None:
        """
        method which gets control over the application (input, output, queries, etc)
        :return:
        """
        raise NotImplementedError
