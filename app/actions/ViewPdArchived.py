from app.actions.AbstractAction import AbstractAction
from app.models import get_session, PersonalCard, Field, FieldType, User


class ViewPdArchived(AbstractAction):
    ACTION_NAME: str = "view-pd-archived"
    COMMAND_NAME: str = "view-pd-archived"

    def handle(self) -> None:
        if not self.have_permission():
           print("You do not have access!")
           return

        session = get_session()
        while True:

            name = input("Input name: ").capitalize()
            surname = input("Input surname: ").capitalize()
            patronymic = input("Input patronymic: ").capitalize()

            if name.isalpha() and surname.isalpha() and patronymic.isalpha():

                query = session.query(PersonalCard, Field, FieldType).filter(PersonalCard.card_id == Field.card_id,
                                                                             Field.field_type_id == FieldType.ft_id,
                                                                             PersonalCard.name == name,
                                                                             PersonalCard.is_archive == True,
                                                                             PersonalCard.surname == surname).all()
                if len(query) == 0:
                    print("Such a student does not exist in the database!")
                    break

                birth_date = query[0][0].birth_date.strftime('%d.%m.%Y')
                print("\nName: {}\nSurname: {}\nPatronymic: {}\nDate of Birth: {}\n".format(query[0][0].name,
                                                                                            query[0][0].surname,
                                                                                            query[0][0].patronymic,
                                                                                            birth_date))
                for i in query:
                    print("{}:\n{}\n".format(i[2].name.capitalize(), i[1].value.decode()))
                break
            print("!!!!!")

