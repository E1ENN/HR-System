import re

VALID_STATUSES = {"NEW", "INTERVIEWED", "REJECTED", "HIRED"}


class CandidateValidator:

    @staticmethod
    def validate_name(full_name: str) -> None:
        name_parts = full_name.strip().split(" ")
        if len(name_parts) < 2 or len(name_parts) > 3:
            raise ValueError("Некорректное ФИО")
        for part in name_parts:
            if len(part) < 2 or not part.isalpha():
                raise ValueError("Некорректное ФИО")

    @staticmethod
    def validate_age(age: int) -> None:
        if not isinstance(age, int) or age < 14 or age > 60:
            raise ValueError("Некорректный возраст")

    @staticmethod
    def validate_email(email: str) -> None:
        email_pattern = r'^[a-zA-Z0-9.]+@[a-z.]+\.[a-z]{2,}$'
        if not re.fullmatch(email_pattern, email):
            raise ValueError("Некорректный email")

    @staticmethod
    def validate_status(status: str) -> None:
        if status.upper() not in VALID_STATUSES:
            raise ValueError("Некорректный статус")