from . import (ViewExtendedPd,
               ViewPdArchived,
               ViewPd,
               EditUser,
               CreateRole,
               CreateUser,
               Help,
               ResetPassword)


def select_action(name):
    """
    function to choose among actions by given command name
    :param name: name to search among present action
    :return: class of found action or None
    """
    cases = {
        "view-extended-pd": ViewExtendedPd,
        "edit-user": EditUser,
        "create-user": CreateUser,
        "create-role": CreateRole,
        "help": Help,
        "view-pd": ViewPd,
        "view-pd-archived": ViewPdArchived
    }
    return cases.get(name) if cases.get(name) is not None else Help
