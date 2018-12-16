from app.actions import Login
from app.actions import select_action
from warnings import warn


class LifeLoop:
    """
    Event loop of the application
    """
    def __init__(self):
        """
        constructor should be used to initialize user session (authentication)
        """
        login = Login()
        login.handle()
        self.user = login.user

    def run(self):
        while True:
            print('_'*80)
            action_class = select_action(input('Type command, \'help\' to display list of commands'))
            action = action_class(self.user)
            if action.have_permission():
                action.handle()
                # action.log_operation()
            else:
                warn("Permission denied")


if __name__ == "__main__":
    loop = LifeLoop()
    loop.run()
