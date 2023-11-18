import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

import hh_api_helpers
import sj_api_helpers

LANGUAGES = [
    "Python",
    "JavaScript",
    "Java",
    "PHP",
    "C++",
    "C#",
    "TypeScript",
    "Kotlin",
    "Go",
    "Swift",
]


def main():
    load_dotenv()
    hh_vacancies_info = hh_api_helpers.get_langs_vacancies_info(LANGUAGES)
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ]
    ]
    for lang, info in hh_vacancies_info.items():
        row = [
            lang,
            str(info['vacancies_found']),
            str(info['vacancies_processed']),
            str(info['average_salary'])
        ]
        table_data.append(row)
    table = AsciiTable(table_data, title="HeadHunter Moscow")
    print(table.table)

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies_info = sj_api_helpers.get_langs_vacancies_info(
        sj_secret_key,
        LANGUAGES
    )
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for lang, info in sj_vacancies_info.items():
        row = [
            lang,
            str(info["vacancies_found"]),
            str(info["vacancies_processed"]),
            str(info["average_salary"]),
        ]
        table_data.append(row)
    table = AsciiTable(table_data, title="SuperJob Moscow")
    print(table.table)


if __name__ == "__main__":
    main()
