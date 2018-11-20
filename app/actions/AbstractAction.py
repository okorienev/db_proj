from abc import abstractmethod, ABCMeta


class AbstractAction(ABCMeta):
    """
    class to declare common interface for console implementation of use cases
    """
    ACTION_NAME: str = None
    COMMAND_NAME: str = None

    @staticmethod
    @abstractmethod
    def have_permission(user) -> bool:
        """
        :param user:
        :return: should return boolean value of user permission
        """
        pass

    @staticmethod
    @abstractmethod
    def handle() -> None:
        """
        method which gets control over the application (input, output, queries, etc)
        :return:
        """
        pass
