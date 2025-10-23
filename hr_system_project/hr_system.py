from time import sleep

from hr_system_project.logger import logger
from hr_system_project.repository import CandidateRepository
from hr_system_project.validator import CandidateValidator


class HRSystem:

    def __init__(self):
        self.repository = CandidateRepository()

    def system_run(self) -> None:
        print("─────────────────────────────────────\n🎯 HR-СИСТЕМА: Управление кандидатами\n─────────────────────────────────────")
        while True:
            self.menu()
            option = input("Выберите опцию >> ")
            try:
                if option == "1":
                    self.add_candidate()
                elif option == "2":
                    self.get_all_candidates()
                elif option == "3":
                    self.find_candidate()
                elif option == "4":
                    self.filter_by_status()
                elif option == "5":
                    self.update_candidate()
                elif option == "6":
                    self.delete_candidate()
                elif option == "7":
                    self.repository.save_to_file()
                    print("Данные сохранены")
                elif option == "8":
                    self.repository.load_from_file()
                    print("Данные загружены")
                elif option == "9":
                    print("Выход...")
                    sleep(1)
                    break
                else:
                    print("Несуществующая опция")
                    sleep(1)
            except ValueError as e:
                logger.error(str(e), exc_info=True)
                print(e)
                sleep(1)

    @staticmethod
    def menu() -> None:
        print(
            "[1] Добавить кандидата\n"
            "[2] Просмотреть всех кандидатов\n"
            "[3] Найти кандидата (по ID или ФИО)\n"
            "[4] Фильтровать по статусу\n"
            "[5] Редактировать кандидата\n"
            "[6] Удалить кандидата\n"
            "[7] Сохранить данные\n"
            "[8] Загрузить данные\n"
            "[9] Выход\n"
            "-----------------------------------"
        )

    def __exit(self):
        while True:
            inp = input("E чтобы выйти >> ")
            if inp.upper() == "E": break

    def delete_candidate(self):
        self.__delete_candidate(input("Удаление по (id/ФИО) >> "))
        self.repository.count += 1

    def __delete_candidate(self, data: str):
        if data.isdigit():
            self.repository.delete_by_id(int(data))
        elif isinstance(data, str):
            self.repository.delete_by_full_name(data)

    def upload_from_file(self):
        self.candidates = self.repository.load_from_file()
        if len(self.candidates) == 0:
            print("Список пуст")
            return
        for id, cand in self.candidates.items():
            print(f"[ID: {id} | {cand}]")
        self.__exit()

    def get_all_candidates(self) -> None:
        if len(self.repository.candidates) == 0:
            print("Список кандидатов пуст")
        else:
            for id, candidate in self.repository.candidates.items():
                print(f"[ID: {id} | {candidate}]")
        self.__exit()

    def filter_by_status(self):
        self.repository.filter_by_status(input("Статус (NEW, INTERVIEWED, REJECTED, HIRED) >> ").upper())
        self.__exit()

    def find_candidate(self):
        self.__find_candidate(input("Поиск (ID/ФИО) >> "))
        self.__exit()

    def __find_candidate(self, data: str):
        if data.isdigit():
            self.repository.find_by_id(int(data))
        elif isinstance(data, str):
            self.repository.find_by_name(data)
        else:
            raise ValueError("Некорректный ввод")

    def update_candidate(self):
        inp = input("Введите ID >> ")
        if not inp.isdigit(): raise ValueError("Ожидается числовое ID")
        id = int(inp)
        if id not in self.repository.candidates: raise ValueError("Кандидат не найден")
        candidate = self.repository.candidates[id]
        print(f"Изменяемая запись: {candidate}")
        full_name = " ".join(part.capitalize() for part in input("Новое ФИО (ENTER чтобы пропустить) >> ").split())
        age_input = input("Новый возраст (ENTER чтобы пропустить) >> ")
        email = input("Новый Email (ENTER чтобы пропустить) >> ")
        status = input("Новый статус (NEW, INTERVIEWED, REJECTED, HIRED) (ENTER чтобы пропустить) >> ")
        self.repository.update_candidate(full_name, age_input, email, status, candidate)
        print("Данные изменены")
        self.repository.count += 1
        sleep(1)

    def add_candidate(self) -> None:
        print("Отмена - E")
        inp = input("ФИО >> ")
        if inp.upper() == "E": return
        full_name = " ".join(part.capitalize() for part in inp.split())
        CandidateValidator.validate_name(full_name)
        inp = input("Возраст (14-60) >> ")
        if inp.upper() == "E": return
        age = inp
        if not age.isdigit(): raise ValueError("Неверный возраст")
        age = int(age)
        CandidateValidator.validate_age(age)
        inp = input("Email >> ")
        if inp.upper() == "E":
            return
        email = inp
        CandidateValidator.validate_email(email)
        inp = input("Статус (NEW, INTERVIEWED, REJECTED, HIRED) >> ")
        if inp.upper() == "E":
            return
        status = inp.upper()
        CandidateValidator.validate_status(status)
        candidate = self.repository.add_candidate(full_name, age, email, status)
        print(f"{candidate.full_name} добавлен")
        self.repository.count += 1
        sleep(1)