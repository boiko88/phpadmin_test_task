# PhpMyAdminScraper

A simple Python script that logs into a remote phpMyAdmin interface and scrapes the `users` table from a selected database using HTTP requests and HTML parsing.

## Features

- Logs in using credentials stored in a `.env` file
- Extracts token for CSRF protection
- Navigates to a target table and extracts `id` and `name` columns
- Saves debugger HTML responses for troubleshooting

Steps:

1 Clone the repo:

git clone https://github.com/boiko88/test_task.git

2 cd test_task

3 Create virtual environment: 

python -m venv venv

venv\Scripts\activate

4 Install dependencies:

pip install -r requirements.txt

5 Run: 

python parser.py 

Alternatively, you can use docker