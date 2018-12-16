from . import AbstractAction


class Help(AbstractAction):
    ACTION_NAME = 'help'
    COMMAND_NAME = 'help'

    def handle(self) -> None:
        print("You are in the \'help\' action")
        print("It happened cause You typed the non-existing command or enterend help manually")
        print("List of cases: " + '\n' + '\n'.join(
            ['%-20s | %-60s' % i for i in
             [("view-extended-pd", "view full personal card(with sensitive info)"),
              ("edit-user", "edit user info"),
              ("create-user", "create new user"),
              ("create-role", "create new user role"),
              ("help", "get help (this case)"),
              ("view-pd", "view short personal card(with no sensitive info)"),
              ("view-pd-archived", "view archived personal card(with personal info)")]]
        ))
