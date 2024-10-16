import json
import os

def get_json_file() -> list[dict, ...]:
    """
    Функция считывает файл Json
    :return: список словарей
    """

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    relative_path = os.path.join(project_root, 'operations', 'operations.json')

    with open(relative_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
