from . import AbstractAction
from app.models import get_session, PersonalCard


class StudentEdit(AbstractAction):
    ACTION_NAME: str = "edit-pd"
    COMMAND_NAME: str = "edit-pd"

    def handle(self):
        session = get_session()
        students = session.query(PersonalCard).all()
        print("You are now in \'edit-pd\' action")

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

                fields = searched_student.fields
                for index, field in enumerate(fields):
                    print("{} : {} ".format(field.field_type.name, field.value.decode("utf-8")))

                while True:
                    choice = int(input(
                        "What do you want to change? \n1 - biography \n2 - nickname \n3 - height \n4 - patronymic "
                        "\n5 - name \n6 - surname \n7 - birth date:"))
                    if choice in range(1, 8):
                        if choice == 1:
                            new_bio = input("Editing biography: ")
                            fields[0].value = new_bio.encode()
                            session.commit()
                            print("Data was successfully updated.")

                        if choice == 2:
                            new_nickname = input("Enter new nickname: ")
                            fields[1].value = new_nickname.capitalize().encode()
                            session.commit()
                            print("Data was successfully updated.")

                        if choice == 3:
                            while True:
                                try:
                                    new_height = int(input("Enter new height: "))
                                    if new_height > 0:
                                        fields[2].value = str(new_height).encode()
                                        session.commit()
                                        print("Data was successfully updated.")
                                    else:
                                        raise ValueError
                                    break
                                except ValueError:
                                    print("Error! Such height is invalid. Try again. ")

                        if choice == 4:
                            new_patronymic = input("Enter new patronymic: ")
                            searched_student.patronymic = new_patronymic.capitalize().encode()
                            session.commit()
                            print("Data was successfully updated.")

                        if choice == 5:
                            new_name = input("Enter new name: ")
                            searched_student.name = new_name.capitalize().encode()
                            session.commit()
                            print("Data was successfully updated.")

                        if choice == 6:
                            new_surname = input("Enter new surname: ")
                            searched_student.surname = new_surname.capitalize().encode()
                            session.commit()
                            print("Data was successfully updated.")

                        if choice == 7:
                            while True:
                                new_birth_day = int(input("Enter new birth day: "))
                                if new_birth_day in range(1, 32):
                                    break
                                else:
                                    print("Incorrect date! Try again.")
                                    continue
                            while True:
                                new_birth_month = int(input("Enter new birth month: "))
                                if new_birth_month in range(1, 13):
                                    break
                                else:
                                    print("Incorrect date! Try again.")
                                    continue
                            while True:
                                new_birth_year = int(input("Enter new birth year: "))
                                if new_birth_year in range(1995, 2002):
                                    break
                                else:
                                    print("Incorrect date! Try again.")
                                    continue
                            searched_student.birth_date = (
                                    str(new_birth_year)+"-" + str(new_birth_month) + "-" + str(new_birth_day)).encode()
                            session.commit()
                            print("Data was successfully updated.")
                        break
                    else:
                        print("There is no such option. Try again! \n")
                        continue
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
