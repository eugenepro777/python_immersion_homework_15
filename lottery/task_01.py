import argparse
import logging

"""
Возьмите любые задания из прошлых домашних заданий.
Добавьте к ним логирование ошибок и полезной информации.
Также реализуйте возможность запуска из командной строки с передачей параметров.
"""


class LotteryGame:
    def __init__(self, ticket_numbers, drawn_numbers):
        self.logger = self.setup_logger()
        self.ticket_numbers = self.get_ticket_numbers(ticket_numbers)
        self.drawn_numbers = self.read_numbers(drawn_numbers)

    def setup_logger(self):

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # сделаем отдельные хендлеры для файла и потока, а потом добавим их в наш logger
        file_handler = logging.FileHandler('logs/lottery_game.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)

        # формат вывода зададим через отдельный класс Formatter и установим его для обоих наших хендлеров
        formatter = logging.Formatter('{levelname:<6} - {asctime} - {filename} - {message}',
                                      style='{', datefmt='%d-%m-%Y %H:%M:%S')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger

    def get_ticket_numbers(self, ticket_numbers):
        try:
            ticket_numbers = [int(num) for num in ticket_numbers.split()]
            self.logger.info(f" Номера в вашем билете: {ticket_numbers}")
            return ticket_numbers
        except ValueError as e:
            self.logger.error(f" Ошибка при получении номеров из билета: {e}")
            exit(1)

    def read_numbers(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                drawn_numbers = [int(num) for num in f.read().split(',')]
            self.logger.info(f" Выигрышные номера: {drawn_numbers}")
            return drawn_numbers
        except FileNotFoundError as e:
            self.logger.error(f" Не найден файл с выигрышными номерами файла: {e}")
            exit(1)
        except ValueError as e:
            self.logger.error(f" Ошибка при чтении выигрышных номеров из файла: {e}")
            exit(1)

    def compare_lists(self):
        matching_numbers = [num for num in self.ticket_numbers if num in self.drawn_numbers]

        if matching_numbers:
            self.logger.info(f" Совпадающие номера в билете: {matching_numbers}")
            self.logger.info(f" Количество совпадающих номеров: {len(matching_numbers)}")
        else:
            self.logger.info(f" Совпадающих номеров нет.")

        return matching_numbers


def parse_args():
    parser = argparse.ArgumentParser(description='Лотерея')
    parser.add_argument('-tn', '--ticket_numbers', type=str, help='Введите номера из билета через пробел')
    parser.add_argument('-dnf', '--drawn_numbers_file',
                        type=str, help='Введите название файла, содержащего выигрышные номера')
    return parser.parse_args()


if __name__ == '__main__':
    # пример запуска командной строкой:python lottery/task_01.py -tn="13 12 8 41 14 15" -dnf="lottery/drawn_numbers.txt"

    args = parse_args()
    try:
        if not args.ticket_numbers or not args.drawn_numbers_file:
            raise ValueError("Укажите и номера из вашего билета, и имя файла, содержащего выигрышные номера")
        game = LotteryGame(args.ticket_numbers, args.drawn_numbers_file)
        matching_numbers = game.compare_lists()
    except ValueError as e:
        print(f"DataError: {e}")
