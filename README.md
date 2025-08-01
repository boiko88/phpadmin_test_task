# PhpMyAdminScraper

A simple Python script that logs into a remote phpMyAdmin interface and scrapes the `users` table from a selected database using HTTP requests and HTML parsing.

## Features

- Logs in using credentials stored in a `.env` file
- Extracts token for CSRF protection
- Navigates to a target table and extracts `id` and `name` columns
- Saves debugger HTML responses for troubleshooting


pip install -r requirements.txt