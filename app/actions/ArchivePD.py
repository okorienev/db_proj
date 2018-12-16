from . import AbstractAction
from app.models import get_session, PersonalCard


class ArchivePD(AbstractAction):
    ACTION_NAME: str = "archive-pd"
    COMMAND_NAME: str = "archive-pd"

    def handle(self):
        session = get_session()
        students = session.query(PersonalCard).all()
        print("You are now in \'archive-pd\' action")

        name_list = []
        surname_list = []
        for i, student in enumerate(students):
            name_list.append(student.name)
            surname_list.append(student.surname)
        while True:
            std_name = input("Enter name: ")
            std_surname = input("Enter surname: ")
            if std_name.capitalize() in name_list and std_surname.capitalize() in surname_list:
                searched_student = session.query(PersonalCard).filter_by(name=std_name.capitalize(),
                                                                         surname=std_surname.capitalize()).first()
                print("Card id: {} \nName: {} \nSurname: {} \nBirth date: {}".format(searched_student.card_id,
                                                                                     searched_student.name,
                                                                                     searched_student.surname,
                                                                                     searched_student.birth_date))

                searched_student.is_archive = 1
                session.commit()
                print("Chosen data was successfully archived.")

                break
            else:
                flag = False
                print("No student found. Try again? (y/n): ")
                while True:
                    choice = input().lower()
                    if choice in 'y':
                        break
                    elif choice in 'n':
                        flag = True
                        break
                    else:
                        print("Try again.")
                        continue
                if flag is True:
                    break
                continue
