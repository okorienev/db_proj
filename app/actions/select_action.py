from . import (ViewExtendedPd,
               ViewPdArchived,
               ViewPd,
               EditUser,
               CreateRole,
               CreateUser,
               Help,
               AddByHand,
               StudentEdit,
               ResetPassword,
               DataExport,
               DataImport,
               ArchivePD)


def select_action(name):
    """
    function to choose among actions by given command name
    :param name: name to search among present action
    :return: class of found action or None
    """
    cases = {
        ViewExtendedPd: ViewExtendedPd,
        EditUser.COMMAND_NAME: EditUser,
        CreateUser.COMMAND_NAME: CreateUser,
        CreateRole.COMMAND_NAME: CreateRole,
        Help.COMMAND_NAME: Help,
        ViewPd.COMMAND_NAME: ViewPd,
        ViewPdArchived.COMMAND_NAME: ViewPdArchived,
        AddByHand.COMMAND_NAME: AddByHand,
        StudentEdit.COMMAND_NAME: StudentEdit,
        ResetPassword.COMMAND_NAME: ResetPassword,
        DataImport.COMMAND_NAME: DataImport,
        DataExport.COMMAND_NAME: DataExport,
        ArchivePD.COMMAND_NAME: ArchivePD
    }
    return cases.get(name) if cases.get(name) is not None else Help
