class AbstractAction:
    """
    class to declare common interface for console implementation of use cases
    """
    ACTION_NAME: str = None
    COMMAND_NAME: str = None

    def __init__(self, user):
        self.user = user

    def have_permission(self) -> bool:
        """
        :return: should return boolean value of current user permission to commit action
        """
        raise NotImplementedError

    def handle(self) -> None:
        """
        method which gets control over the application (input, output, queries, etc)
        :return:
        """
        raise NotImplementedError
