from time import sleep
from typing import Dict, List
from hr_system_project.validator import CandidateValidator
import json

DB_FILE_NAME = "hr_system_project/database.json"


class Candidate:

    def __init__(self, full_name: str, age: int, email: str, status: str):
        self.full_name = full_name
        self.age = age
        self.email = email
        self.status = status

    def __repr__(self):
        return f"ФИО: {self.full_name} | Возраст: {self.age} | Email: {self.email} | Статус: {self.status}"

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "age": self.age,
            "email": self.email,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Candidate(data["full_name"], data["age"], data["email"], data["status"])


class CandidateRepository:

    def __init__(self):
        self.candidates = self.load_from_file()
        self.count = 0

    def add_candidate(self, full_name: str, age: int, email: str, status: str) -> 'Candidate':
        candidate = Candidate(full_name, age, email, status)
        self.candidates[len(self.candidates) + 1] = candidate
        return candidate

    def find_by_name(self, name) -> List[str]:
        lst_candidates = list()
        for id, candidate in self.candidates.items():
            if name in candidate.full_name:
                lst_candidates.append(f"[ID: {id} | {candidate}]")
        for el in lst_candidates:
            print(el)
        print(f"Найдено {len(lst_candidates)} записей")
        return lst_candidates


    def find_by_id(self, cid) -> 'Candidate':
        for id, candidate in self.candidates.items():
            if cid == id:
                print(f"[ID: {id} | {candidate}]")
                return candidate
        print("Запись не найдена")

    def filter_by_status(self, status) -> List[str] | None:
        CandidateValidator.validate_status(status)
        lst_statuses = list()
        for id, candidate in self.candidates.items():
            if candidate.status == status:
                lst_statuses.append(f"[ID: {id} | {candidate}]")
        if len(lst_statuses) == 0:
            print(f"Нет записей со статусом {status}")
            return
        for el in lst_statuses:
            print(el)
        return lst_statuses

    def update_candidate(self, full_name, age, email, status, candidate: 'Candidate') -> 'Candidate':
        if full_name == "" and age == "" and email == "" and status == "": raise ValueError("Нет изменений")
        full_name = full_name if full_name != "" else candidate.full_name
        CandidateValidator.validate_name(full_name)
        if age == "":
            age = int(candidate.age)
        elif not age.isdigit():
            raise ValueError("Возраст должен быть числом")
        CandidateValidator.validate_age(int(age))
        email = email if email != "" else candidate.email
        CandidateValidator.validate_email(email)
        status = status if status != "" else candidate.status
        CandidateValidator.validate_status(status)
        candidate.full_name, candidate.age, candidate.email, candidate.status = full_name, int(age), email, status
        return candidate

    def delete_by_id(self, cid) -> 'Candidate':
        if cid not in self.candidates: raise ValueError("Кандидат не найден")
        candidate = self.candidates[cid]
        del self.candidates[cid]
        print("Запись удалена")
        sleep(1)
        return candidate

    def delete_by_full_name(self, full_name) -> None:
        deleted_id = None
        for id, candidate in self.candidates.items():
            if full_name == candidate.full_name:
                deleted_id = id
                break
        if deleted_id == None: raise ValueError("Кандидат не найден")
        del self.candidates[deleted_id]
        print("Запись удалена")
        sleep(1)

    def save_to_file(self) -> Dict:
        with open(DB_FILE_NAME, "w", encoding="utf-8") as file:
            data = {cid: candidate.to_dict() for cid, candidate in self.candidates.items()}
            json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Сохранено изменений {self.count}")
            self.count = 0
            sleep(1)
            return data

    def load_from_file(self) -> Dict:
        try:
            with open(DB_FILE_NAME, "r", encoding="utf-8") as file:
                candidates = {int(cid): Candidate.from_dict(candidate) for cid, candidate in json.load(file).items()}
                self.candidates = candidates
                return candidates
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return dict()
