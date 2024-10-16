import json
from operator import itemgetter
import os


def get_json_file() -> list[dict, ...]:
    """
    Функция считывает файл Json.
    :return: список словарей.
    """

    # Получение абсолютного пути к текущему файлу
    current_file_path = os.path.abspath(__file__)
    # Переход на уровень выше, к корню проекта
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    # Создание относительного пути к файлу operations.json
    relative_path = os.path.join(project_root, 'operations', 'operations.json')

    with open(relative_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def get_list_completed_operations(list_new: list[dict, ...]) -> list[dict, ...]:
    """
    Функция принимает список словарей и сортирует его по выполненным операциям.
    :param list_new: список словарей.
    :return: список словарей.
    """

    completed_operations = []
    for operation in list_new:
        if operation.get("state") == "EXECUTED":
            completed_operations.append(operation)
    return completed_operations


def get_latest_transactions(list_new: list[dict, ...]) -> list[dict, ...]:
    """
    Функция принимает список словарей и отсортировывает их по дате, возвращая
    только пять последних операций по дате.
    :param list_new: список словарей.
    :return: пять первых элементов в списке.
    """

    # Сортируем список словарей по ключу "date" в порядке убывания
    sorted_list = sorted(list_new, key=itemgetter("date"), reverse=True)

    # Добавляем первые пять элементов из отсортированного списка в новый список
    latest_transactions = []
    for i in range(min(5, len(sorted_list))):
        latest_transactions.append(sorted_list[i])

    return latest_transactions


def get_date_from_string(list_new: list[dict, ...]) -> tuple[str, ...]:
    """
    Функция принимает список словарей и возвращает кортеж из дат и типов операций.
    :param list_new: список словарей.
    :return: кортеж строк.
    """

    date = [data["date"][:10].replace("-", ".") for data in list_new]
    list_operations = [description["description"] for description in list_new]
    revers_data = [".".join(data.split(".")[::-1]) for data in date]
    type_transaction = (f"{revers_data[0]} + {list_operations[0]}",
                        f"{revers_data[1]} +  + {list_operations[1]}",
                        f"{revers_data[2]} +  + {list_operations[2]}",
                        f"{revers_data[3]} +  + {list_operations[3]}",
                        f"{revers_data[4]} + ' ' + {list_operations[4]}")

    return type_transaction


def get_card_number(list_new: list[dict, ...]) -> tuple[str, ...]:
    """
    Функция принимает список словарей и возвращает зашифрованное значение по ключу "from".
    :param list_new: список словарей.
    :return: кортеж строк.
    """

    list_cards = [card.get("from") for card in list_new]
    list_number = [number.split()[-1] for number in list_cards if number is not None]
    cards_number = [number[:6] + "*" * 6 + number[-4:] for number in list_number if len(number) < 20]
    hidden_numbers = ("".join([f"{cards_number[0][:4]} {cards_number[0][4:8]} {cards_number[0][8:12]} {cards_number[0][12:16]},"
                      f"{cards_number[1][:4]} {cards_number[1][4:8]} {cards_number[1][8:12]} {cards_number[1][12:16]}"])
                      .split(","))
    hidden_numbers.append("**" + list_number[2][len(list_number[2]) - 4:])

    empty_list = []
    for card in list_cards:
        if card is not None:
            for el in card:
                if el.isalpha():
                    empty_list.append(el)

    card_names = f"{''.join(empty_list)[:11]} {''.join(empty_list)[11:18]} {''.join(empty_list)[18:]}".split()
    hidden_information = (f"{None}",
                          f"{card_names[0][:4]} {card_names[0][4:11]} {hidden_numbers[0]}",
                          f"{card_names[1]} {hidden_numbers[1]}",
                          f"{card_names[2]} {hidden_numbers[2]}",
                          f"{None}")

    return hidden_information


def get_account_number(list_new: list[dict, ...]) -> list[str, ...]:
    """
    Функция получает список из 5 последних операций и выводит замаскированный счет куда были отправлены деньги.
    :param list_new: список словарей.
    :return: список строк
    """

    account = [to.get("to").split()[0] + " " for to in list_new]
    hidden_account = [account[0] + "**" + to.get("to").split()[-1][len(to.get("to").split()[-1]) - 4:] for to in list_new]

    return hidden_account


def get_amount_transactions(list_new: list[dict, ...]) -> list[str, ...]:
    """
    Функция получает список из 5 последних операций и возвращает список из сумм и валюты
    выполненных операций.
    :param list_new: список словарей.
    :return: список строк.
    """

    summ = [summ.get("operationAmount")["amount"] + " " + summ.get("operationAmount")["currency"]["name"] for summ in list_new]
    return summ