from datetime import datetime
from app.actions.AbstractAction import AbstractAction
from app.models import get_session, PersonalCard, Field, FieldType, User
import warnings


class AddByHand(AbstractAction):
    ACTION_NAME: str = "add-by-hand"
    COMMAND_NAME: str = "add-by-hand"

    def handle(self) -> None:
        if not self.have_permission():
             print("You do not have permissions to perform this action.")
             return
        while True:
            name = input("Input name: ").capitalize()
            surname = input("Input surname: ").capitalize()
            patronymic = input("Input patronymic: ").capitalize()
            birth_date = input("Input birth date: ")
            archive = input("Is archive data? (press '+' or '-'): ")

            try:
                birth_datetime = datetime.strptime(birth_date, '%d.%m.%Y').date()
            except ValueError:
                warnings.warn("Incorrect date format")
                continue
            else:
                if name.isalpha() and surname.isalpha() and archive in ["+", "-"]:
                    if archive == "+":
                        is_archive = True
                    else:
                        is_archive = False

                    session = get_session()
                    if len(session.query(PersonalCard).filter(PersonalCard.name == name,
                                                              PersonalCard.surname == surname,
                                                              PersonalCard.patronymic == patronymic).all()) == 0:

                        personal_card = PersonalCard(name=name.capitalize(),
                                                     surname=surname.capitalize(),
                                                     patronymic=patronymic.capitalize(),
                                                     birth_date=birth_datetime,
                                                     is_archive=is_archive)

                        session.add(personal_card)

                        field_types = session.query(FieldType).all()
                        for i in field_types:
                            value  = input("Write a {}:\n".format(i.name))
                            session.add(Field(field_type=i, value=value.encode(), card=personal_card))
                        session.commit()
                        print("New student added to base!")
                        break

                    else:
                        print("Such a student already exists in the database.")
            print("!!!!!")
