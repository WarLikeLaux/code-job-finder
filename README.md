<a name="readme-top"></a>

# Code Job Finder

<details>
<summary><h2>Table of Contents</h2></summary>

  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project objectives](#project-objectives)
  - [License](#license)
</details>

## Overview

**Code Job Finder** is a powerful tool designed to aggregate programming job vacancies from major Russian job platforms, HeadHunter and SuperJob. It allows users to retrieve and analyze job market data, focusing on the demand for various programming languages in Moscow. The application provides insightful statistics such as the number of vacancies found, vacancies processed, and the average salary offered, thus offering a comprehensive view of the current job market for programmers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

- **Vacancy Data Aggregation:** gathers information about programming job vacancies from HeadHunter and SuperJob APIs.
- **Support for Multiple Programming Languages:** tracks job vacancies for popular programming languages like Python, JavaScript, Java, PHP, C++, C#, TypeScript, Kotlin, Go, and Swift.
- **Analytical Insights:** offers detailed analysis including the number of vacancies found, processed, and average salaries for each programming language.
- **User-Friendly Data Presentation:** utilizes the AsciiTable library to present data in an easy-to-read table format.
- **Environment Variable Configuration:** uses environment variables such as `SJ_SECRET_KEY` for secure API interactions.
- **Simple Installation and Usage:** easy to set up and use, requiring only basic Python knowledge and environment setup.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

To install Code Job Finder, follow these steps:

### 1. 🐍 Environment setup

First of all, make sure you have Python 3 installed, version `3.8.0` or higher. If not, visit the [official Python website](https://www.python.org/) and download the latest version.

The command to check your Python version should show a version no lower than `3.5.0`. You might need to use aliases such as `python`, `py`, `python3.8`, or onwards up to `python3.12` instead of `python3`.

```
$ python --version
Python 3.8.10
```

### 2. 📥 Repository cloning

Clone the repository using the command below:

```
git clone https://github.com/WarLikeLaux/code-job-finder
```

Then, navigate to the project folder:

```
cd code-job-finder
```

### 3. 🧩 Dependencies installation

Use pip (or pip3, if there's a conflict with Python2) to install the dependencies:

```
pip install -r requirements.txt
```

### 4. 🗝️ Environment variables setup

To set up your environment variables, you'll need to create a `.env` file in the root directory of the project. If you already have a `.env.example` file, you can simply copy with rename it to `.env` using the command `cp .env.example .env`. Once you've done this, add or/and fill the following lines by values in your `.env` file:

- `SJ_SECRET_KEY`: this key serves as your unique identifier for accessing the SuperJob API. It enables the retrieval of job vacancy data from the SuperJob platform. To obtain your personal API key, register at the [official SuperJob website](https://api.superjob.ru/register). This key is essential for authenticating your requests to the SuperJob API and accessing detailed vacancy information.

Please ensure that each environment variable is assigned the correct value.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

To operate Code Job Finder, follow these steps:

**1. Retrieving Vacancy Information by Programming Language in Moscow from HeadHunter and SuperJob:**

Execute the following command in your terminal to gather data about programming job vacancies in Moscow. The script fetches information separately from HeadHunter and SuperJob APIs.

```
python main.py
```

**Example of script output:**

```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 1469             | 33                  | 91073            |
| JavaScript            | 2599             | 30                  | 80530            |
| Java                  | 935              | 34                  | 81514            |
| PHP                   | 1797             | 32                  | 77546            |
| C++                   | 1076             | 38                  | 147380           |
| C#                    | 881              | 34                  | 75822            |
| TypeScript            | 770              | 35                  | 131168           |
| Kotlin                | 227              | 37                  | 149108           |
| Go                    | 313              | 31                  | 154016           |
| Swift                 | 140              | 36                  | 160691           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 2                | 2                   | 180000           |
| JavaScript            | 2                | 2                   | 120000           |
| Java                  | 2                | 2                   | 97250            |
| PHP                   | 13               | 8                   | 135302           |
| C++                   | 5                | 5                   | 187400           |
| C#                    | 5                | 2                   | 162000           |
| TypeScript            | 0                | 0                   | 0                |
| Kotlin                | 0                | 0                   | 0                |
| Go                    | 0                | 0                   | 0                |
| Swift                 | 0                | 0                   | 0                |
+-----------------------+------------------+---------------------+------------------+
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Project objectives

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This code is open-source and free for any modifications, distributions, and uses. Feel free to utilize it in any manner you see fit.

<p align="right">(<a href="#readme-top">back to top</a>)</p>