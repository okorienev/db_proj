import json, os

from app.actions import AbstractAction
from app.models import get_session, PersonalCard, Field


class DataExport(AbstractAction):

    ACTION_NAME = 'export-pd'
    COMMAND_NAME = 'export-pd'

    def handle(self) -> None:
        session = get_session()
        while True:
            file_path = input('json file for export?:')
            if not file_path.endswith('json'):
                print('wrong file type..')
                continue
            self.__exporter(file_path, session)
            break

    @staticmethod
    def __exporter(file_path, ses):
        while True:
            try:
                file = open(file_path, 'x+')

                query_pc = ses.query(PersonalCard)

                data = []
                for i in query_pc:
                    query_f = ses.query(Field).filter_by(
                        card_id=i.card_id
                    ).order_by(Field.field_type_id)

                    data.append({'name': i.name,
                                 'surname': i.surname,
                                 'patronymic': i.patronymic,
                                 'birth_date': str(i.birth_date),
                                 'fields': {
                                     key: value.value.decode() for (key, value) in zip(
                                      ('biography', 'nickname', 'height'), query_f)
                                 }})

                json.dump(data, file, indent=4, sort_keys=True)

                file.close()
                break
            except FileExistsError:
                os.remove(file_path)
                print('deleted previous file')
                continue
