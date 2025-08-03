import requests
import os
from bs4 import BeautifulSoup
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


class PhpMyAdminScraper:
    """
    A scraper to log into phpMyAdmin and extract data from the 'users' table.

    Environment Variables Used:
        - LOGIN_LINK: URL to phpMyAdmin login page.
        - DB_LINK: URL to the database view.
        - TABLE_LINK: URL to the specific table view.

    Attributes:
        username (str): Login username.
        password (str): Login password.
        session (requests.Session): Persistent session for requests.
        token (str): CSRF token required by phpMyAdmin.
    """

    def __init__(self, username: str, password: str):
        self.login_link = os.getenv('LOGIN_LINK')
        self.db_link = os.getenv('DB_LINK')
        self.table_link = os.getenv('TABLE_LINK')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = ''

    # Saves an HTML file to make sure data you try to scrape is reached
    def debugger(self, filename: str, html: str):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html)
            print(f'Saved HTML to file: {filename}')
        except Exception as e:
            print(f'There was an {e} error')

    def get_token(self, html: str, context: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})
        if not token_input:
            print(f'Token not found during {context}.')
            self.debugger(f'debug_token_{context}.html', html)
            exit()
        return token_input['value']

    def login(self):
        try:
            resp = self.session.get(self.login_link)
            self.token = self.get_token(resp.text, 'before_login')
            print(f'Token for login: {self.token}')
        except requests.RequestException as e:
            print(f'There was an {e} error')

        login_payload = {
            'pma_username': self.username,
            'pma_password': self.password,
            'server': 1,
            'target': 'index.php',
            'lang': 'ru',
            'token': self.token
        }
        # Mimic real browser
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        resp = self.session.post(
            self.login_link,
            data=login_payload,
            headers=headers
            )
        if 'phpMyAdmin' not in resp.text:
            print('Authorization failed')
            self.debugger('debug_auth_fail.html', resp.text)
            exit()

        print('Authorization successful')

        # Refresh token after login
        resp = self.session.get(self.login_link)
        self.token = self.get_token(resp.text, 'after_login')
        print(f'Your New Token: {self.token}')

    def get_users_table(self):
        # Mimic real browser
        headers_with_referer = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': self.login_link
        }

        self.session.get(
            self.db_link + f'&token={self.token}',
            headers=headers_with_referer
            )
        table_url = self.table_link + f'&token={self.token}'
        resp = self.session.get(table_url, headers=headers_with_referer)
        print(f'Table status is: {resp.status_code}')
        self.debugger('debugger.html', resp.text)

        soup = BeautifulSoup(resp.text, 'html.parser')
        # Look for the table that contains the results
        table = soup.find('table', {'class': 'table_results'})

        if not table:
            print('Users table not found')
            exit()

        # Extract rows from the table, skip the header row
        rows = table.find_all('tr')[1:]
        data = []

        # Column positions (may vary by phpMyAdmin setup)
        ID_COLUMN_INDEX = -2
        NAME_COLUMN_INDEX = -1
        MIN_EXPECTED_COLUMNS = 2

        for r in rows:
            cols = r.find_all('td')
            if len(cols) >= MIN_EXPECTED_COLUMNS:
                id_val = cols[ID_COLUMN_INDEX].get_text(strip=True)
                name_val = cols[NAME_COLUMN_INDEX].get_text(strip=True)
                data.append([id_val, name_val])

        print('Users Table:\n')
        pprint(data)


if __name__ == '__main__':
    try:
        username = os.getenv('PMA_LOGIN')
        password = os.getenv('PMA_PASSWORD')

        if not username or not password:
            print('PMA_LOGIN or PMA_PASSWORD is not set in .env file.')
            exit()

        scraper = PhpMyAdminScraper(
            username=username,
            password=password
        )
        scraper.login()
        scraper.get_users_table()
        
    except Exception as e:
        print(f'There was an {e} error')
