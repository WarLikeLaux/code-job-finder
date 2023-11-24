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
    hh_max_pages = int(os.environ["HH_MAX_PAGES"])
    hh_timeout = int(os.environ["HH_TIMEOUT"])
    hh_vacancies_info = hh_api_helpers.get_langs_vacancies_info(
        LANGUAGES,
        hh_max_pages,
        hh_timeout
    )
    hh_table_data = [
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
            info['vacancies_found'],
            info['vacancies_processed'],
            info['average_salary']
        ]
        hh_table_data.append(row)
    hh_table = AsciiTable(hh_table_data, title="HeadHunter Moscow")
    print(hh_table.table)

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies_info = sj_api_helpers.get_langs_vacancies_info(
        sj_secret_key,
        LANGUAGES
    )
    sj_table_data = [
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
            info["vacancies_found"],
            info["vacancies_processed"],
            info["average_salary"],
        ]
        sj_table_data.append(row)
    sj_table = AsciiTable(sj_table_data, title="SuperJob Moscow")
    print(sj_table.table)


if __name__ == "__main__":
    main()
