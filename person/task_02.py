import re
import argparse
import logging

"""
Возьмите любые задания из прошлых домашних заданий.
Добавьте к ним логирование ошибок и полезной информации.
Также реализуйте возможность запуска из командной строки с передачей параметров.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/person_employee.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

# формат вывода зададим через отдельный класс Formatter и установим его для обоих наших хендлеров
formatter = logging.Formatter('{levelname:<6} - {asctime} - {message}', style='{', datefmt='%d-%m-%Y %H:%M:%S')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class InvalidNameError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Недопустимое имя: {self.name}. Только символы алфавита. Не должно быть пустой строкой.'


class InvalidAgeError(Exception):
    def __init__(self, age):
        self.age = age

    def __str__(self):
        return f'Возраст задан неверно'


class InvalidIdError(Exception):
    def __init__(self, e_id):
        self.e_id = e_id

    def __str__(self):
        return f'Неверный ID: {self.e_id}. Должен быть положительным целым числом в диапазоне от 100000 до 999999.'


class Person:
    def __init__(self, last_name, first_name, patronymic, age):
        self._validate_name(last_name)
        self._validate_name(first_name)
        self._validate_name(patronymic)
        self._validate_age(age)
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.age = age

        logger.info(f'Создан объект Person: {self.__str__()}')

    def _validate_name(self, name):
        if not isinstance(name, str) or not re.match(r'^[A-Za-zА-Яа-я]+$', name) or len(name.strip()) == 0:
            logger.error(f"Ошибка в имени: {name} или пустое имя")
            raise InvalidNameError(name)

    def _validate_age(self, age):
        if not isinstance(age, int) or age <= 0:
            logger.error(f"Ошибочно задан возраст: {age}")
            raise InvalidAgeError(age)

    def get_age(self):
        return self.age

    def birthday(self):
        self.age += 1

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}, возраст: {self.age}'

    def __repr__(self):
        return f'Person("{self.last_name}", "{self.first_name}", "{self.patronymic}", {self.age})'


class Employee(Person):

    def __init__(self, last_name, first_name, patronymic, age, employee_id):
        self.employee_id = self._validate_employee_id(employee_id)
        self._access_level = self.calculate_access_level()
        super().__init__(last_name, first_name, patronymic, age)

        logger.info(f'Создан объект Employee: {self.__str__()}')

    def get_level(self):
        return self._access_level

    @staticmethod
    def _validate_employee_id(employee_id):
        if not (isinstance(employee_id, int) and 100000 <= employee_id <= 999999):
            logger.error(
                f"Неверный ID: {employee_id}. Должен быть положительным целым числом в диапазоне от 100000 до 999999.")
            raise InvalidIdError(employee_id)
        return employee_id

    def calculate_access_level(self):
        sum_digits = sum(int(digit) for digit in str(self.employee_id))
        return sum_digits % 7

    def __str__(self):
        return f'{super().__str__()}, ID: {self.employee_id}, уровень доступа: {self.get_level()}'

    def __repr__(self):
        return f'Employee("{self.last_name}", "{self.first_name}", "{self.patronymic}", {self.age}, {self.employee_id})'


# выбор варианта объекта для создания через командную строку
def create_person_or_employee(args):
    if args.type == 'P':
        return Person(args.ln, args.fn, args.p, args.a)
    elif args.type == 'E':
        return Employee(args.ln, args.fn, args.p, args.a, args.id)


def main():
    parser = argparse.ArgumentParser(description='Создание объектов Person или Employee')
    parser.add_argument('-t', dest='type', choices=['P', 'E'],
                        required=True, help='Выбор объекта (P для Person, E для Employee)')
    parser.add_argument('-ln', dest='ln', type=str, required=True, help='Фамилия')
    parser.add_argument('-fn', dest='fn', type=str, required=True, help='Имя')
    parser.add_argument('-p', dest='p', type=str, required=True, help='Отчество')
    parser.add_argument('-a', dest='a', type=int, required=True, help='Возраст')
    parser.add_argument('-id', dest='id', type=int,
                        help='Employee ID (только для Employee)')

    args = parser.parse_args()

    try:
        obj = create_person_or_employee(args)
        print(obj)
    except (InvalidNameError, InvalidAgeError, InvalidIdError) as e:
        print(f"Ошибка создания объекта: {e}")


if __name__ == '__main__':
    # пример запуска командной строкой:
    # python person/task_02.py -t='P' -ln='Яковлев' -fn='Федор' -p='Сергеевич' -a='32'
    # пример запуска командной строкой:
    # python person/task_02.py -t='E' -ln='Иванов' -fn='Иван' -p='Васильевич' -a='19' -id='345215'
    main()
