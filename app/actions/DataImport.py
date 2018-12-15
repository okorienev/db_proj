import json

from app.actions import AbstractAction
from app.models import get_session, PersonalCard


class DataImport(AbstractAction):

    ACTION_NAME = 'import-pd'
    COMMAND_NAME = 'import-pd'

    def handle(self) -> None:
        session = get_session()
        while True:
            file_path = input('json file for input?:')
            if not file_path.endswith('json'):
                print('wrong file type..')
                continue
            self.__importer(file_path, session)
            break
        session.commit()

    @staticmethod
    def __importer(file_path, ses):
        try:
            file = open(file_path, 'r')

            data = json.load(file)

            for card in data:
                ses.add(PersonalCard(**card))
                print(card)

            file.close()
        except FileNotFoundError:
            print('error opening file...')
